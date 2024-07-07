# your_app/views.py
from django.shortcuts import render, get_object_or_404
from .models import Post

def news_list(request):
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'news_list.html', {'posts': posts})

def news_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    return render(request, 'news_detail.html', {'post': post})
