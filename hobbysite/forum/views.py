from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def threads_list(request):
    return render(request, 'forum/threads_list.html')

def thread_detail(request):
    return render(request, 'forum/thread_detail.html')