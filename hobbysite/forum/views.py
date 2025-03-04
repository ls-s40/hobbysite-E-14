from django.shortcuts import render
from django.http import HttpResponse
from .models import Post, PostCategory

# Create your views here.

def threads_list(request,):
    postcategories = PostCategory.objects.all()
    ctx = {
        'postcategories': postcategories
    }

    return render(request, 'forum/threads_list.html', ctx)

def thread_detail(request, id):
    category = PostCategory.objects.get(id=id)
    posts = Post.objects.filter(category=category)
    ctx = {
        'posts': posts,
    }
    return render(request, 'forum/thread_detail.html', ctx)