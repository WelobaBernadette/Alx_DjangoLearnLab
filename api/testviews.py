from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from api.models import Author, Book

class BookAPITestCase(APITestCase):
    def setUp(self):
        # Create a user for authentication
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.client.login(username="testuser", password="testpass")

        # Create an author and books
        self.author = Author.objects.create(name="Author One")
        self.book1 = Book.objects.create(title="Book One", publication_year=2001, author=self.author)
        self.book2 = Book.objects.create(title="Book Two", publication_year=2010, author=self.author)

        # Endpoints
        self.list_url = reverse("book-list")
        self.detail_url = lambda pk: reverse("book-detail", kwargs={"pk": pk})

    def test_list_books(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_create_book(self):
        data = {
            "title": "Book Three",
            "publication_year": 2020,
            "author": self.author.id
        }
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 3)

    def test_update_book(self):
        data = {
            "title": "Book One Updated",
            "publication_year": 2005,
            "author": self.author.id
        }
        response = self.client.put(self.detail_url(self.book1.id), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, "Book One Updated")

    def test_delete_book(self):
        response = self.client.delete(self.detail_url(self.book2.id))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 1)

    def test_filter_books_by_title(self):
        response = self.client.get(f"{self.list_url}?title=Book One")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(all("Book One" in book["title"] for book in response.data))

    def test_search_books(self):
        response = self.client.get(f"{self.list_url}?search=Two")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(any("Two" in book["title"] for book in response.data))

    def test_order_books_by_year(self):
        response = self.client.get(f"{self.list_url}?ordering=publication_year")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        years = [book["publication_year"] for book in response.data]
        self.assertEqual(years, sorted(years))
