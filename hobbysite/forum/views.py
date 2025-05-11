"""Manages the different views of the forum app."""

from django.shortcuts import render
from .models import Thread, ThreadCategory

# Create your views here.


def thread_list(request,):
    """Return render of list view page using PostCategory model."""
    threadcategories = ThreadCategory.objects.all().order_by('name')
    ctx = {
        'threadcategories': threadcategories
    }

    return render(request, 'forum/thread_list.html', ctx)


def thread_detail(request, id):
    """Return render of detail view page using Post and PostCateogry models."""
    category = ThreadCategory.objects.get(id=id)
    threads = Thread.objects.filter(category=category).order_by('-created_on').values()
    ctx = {
        'threads': threads,
        'category': category
    }
    return render(request, 'forum/thread_detail.html', ctx)
