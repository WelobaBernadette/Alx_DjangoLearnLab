from django.db import models
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    published_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        permissions = [
            ("can_view_books", "Can view list of books"),
            ("can_edit_books", "Can edit books"),
        ]


class BookAudit(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    action = models.CharField(max_length=255)
    performed_by = models.CharField(max_length=255)
    performed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.performed_by} {self.action} {self.book.title}"
