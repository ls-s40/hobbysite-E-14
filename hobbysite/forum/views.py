"""Manages the different views of the forum app."""

from django.shortcuts import render
from .models import Post, PostCategory

# Create your views here.


def thread_list(request,):
    """Return render of list view page using PostCategory model."""
    postcategories = PostCategory.objects.all().order_by('name')
    ctx = {
        'postcategories': postcategories
    }

    return render(request, 'forum/thread_list.html', ctx)


def thread_detail(request, id):
    """Return render of detail view page using Post and PostCateogry models."""
    category = PostCategory.objects.get(id=id)
    posts = Post.objects.filter(category=category).order_by('-created_on').values()
    ctx = {
        'posts': posts,
        'category': category
    }
    return render(request, 'forum/thread_detail.html', ctx)
