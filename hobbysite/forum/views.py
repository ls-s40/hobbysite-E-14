"""Manages the different views of the forum app."""

from django.shortcuts import get_object_or_404, render
from .models import Thread, ThreadCategory

# Create your views here.


def thread_list(request,):
    """Return render of list view page using PostCategory model."""
    threadcategories = ThreadCategory.objects.all().order_by('name')
    threads = Thread.objects.all()
    ctx = {
        'threadcategories': threadcategories,
        'threads': threads
    }

    return render(request, 'forum/thread_list.html', ctx)


def thread_detail(request, id):
    """Return render of detail view page using Thread and ThreadCateogry models."""
    thread = get_object_or_404(Thread, id=id)
    ctx = {
        'thread': thread
    }
    return render(request, 'forum/thread_detail.html', ctx)
