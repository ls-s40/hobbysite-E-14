"""Manages the different views of the forum app."""

from django.shortcuts import get_object_or_404, render, redirect
from .models import Thread, ThreadCategory
from django.contrib.auth.decorators import login_required
from user_management.models import Profile
from .forms import ThreadForm, CommentForm

# Create your views here.


def thread_list(request):
    """Return render of list view page using PostCategory model."""
    threadcategories = ThreadCategory.objects.all().order_by('name')

    user_threads = None
    all_threads = Thread.objects.all().select_related('category').order_by('-created_on')

    if request.user.is_authenticated:
        try:
            current_user = Profile.objects.get(user=request.user)
            user_threads = Thread.objects.filter(author=current_user).order_by('-created_on')
            all_threads = all_threads.exclude(author=current_user)
        except Profile.DoesNotExist:
            pass


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
    comments = thread.forum_comments.all()

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.thread = thread
            comment.author = Profile.objects.get(user=request.user)
            comment.save()
            return redirect(thread.get_absolute_url())
    else:
        form = CommentForm()

    ctx = {
        'thread': thread,
        'comments': comments,
        'other_threads': other_threads,
        'form':form
    }
    return render(request, 'forum/thread_detail.html', ctx)

@login_required
def create_thread(request):
    """Generate view to add a thread."""
    if request.method == 'POST':
        form = ThreadForm(request.POST, request.FILES)
        if form.is_valid():
            thread = form.save(commit=False)
            thread.author = Profile.objects.get(user=request.user)
            thread.save()
            return redirect(thread.get_absolute_url())
    else:
        form = ThreadForm()

    ctx = {'form': form}
    return render(request, 'forum/add_thread.html', ctx)

@login_required
def edit_thread(request, id):
    thread = get_object_or_404(Thread, id=id)

    if thread.author != Profile.objects.get(user=request.user):
        return redirect('forum:index')
    
    if request.method == 'POST':
        form = ThreadForm(request.POST, request.FILES, instance=thread)
        if form.is_valid():
            form.save()
            return redirect(thread.get_absolute_url())
    else:
        form = ThreadForm(instance=thread)

    ctx = {
        'form': form,
        'thread': thread
        }
    return render(request, 'forum/edit_thread.html', ctx)
