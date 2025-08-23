from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import Post, Tag
from .forms import PostForm
from django.contrib.auth.decorators import login_required

def post_list(request):
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'blog/post_list.html', {'posts': posts})

@login_required
def post_create(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            form.save_m2m()
            return render(request, "blog/post_detail.html", {"post": post})
    else:
        form = PostForm()
    return render(request, "blog/post_form.html", {"form": form})

def search_posts(request):
    query = request.GET.get("q")
    results = []
    if query:
        results = Post.objects.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(tags__name__icontains=query)
        ).distinct()
    return render(request, "blog/search_results.html", {"results": results, "query": query})

def posts_by_tag(request, tag_name):
    tag = get_object_or_404(Tag, name=tag_name)
    posts = tag.posts.all()
    return render(request, "blog/post_list.html", {"posts": posts, "tag": tag})
