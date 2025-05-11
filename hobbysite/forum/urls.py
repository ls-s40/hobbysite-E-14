"""Manages the URL pathing of the forum app."""

from django.urls import path
from .views import thread_list, thread_detail, create_thread

urlpatterns = [
        path('threads/', thread_list, name='index'),
        path('thread/<int:id>/', thread_detail, name='thread_detail'),
        path('thread/add/', create_thread, name="create_thread")
    ]

app_name = "forum"
