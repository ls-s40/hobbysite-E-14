"""Manages the different views of the forum app."""

from django.shortcuts import get_object_or_404, render
from .models import Thread, ThreadCategory
from django.contrib.auth.decorators import login_required
from user_management.models import Profile

# Create your views here.

@login_required
def thread_list(request):
    """Return render of list view page using PostCategory model."""
    threadcategories = ThreadCategory.objects.all().order_by('name')

    current_user = Profile.objects.get(user=request.user)
    user_threads = Thread.objects.filter(author=current_user).order_by('-created_on')

    all_threads = Thread.objects.exclude(author=current_user).select_related('category')


    ctx = {
        'threadcategories': threadcategories,
        'user_threads': user_threads,
        'all_threads': all_threads
    }

    return render(request, 'forum/thread_list.html', ctx)


def thread_detail(request, id):
    """Return render of detail view page using Thread and ThreadCateogry models."""
    thread = get_object_or_404(Thread, id=id)
    category = thread.category
    other_threads = Thread.objects.filter(category=category).exclude(id=thread.id)

    comments = thread.comments.all()
    ctx = {
        'thread': thread,
        'comments': comments,
        'other_threads': other_threads
    }
    return render(request, 'forum/thread_detail.html', ctx)
