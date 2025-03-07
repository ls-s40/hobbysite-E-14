"""Manages the URL pathing of the forum app."""

from django.urls import path
from .views import threads_list, thread_detail

urlpatterns = [
        path('threads/', threads_list, name='threads_list'),
        path('thread/<int:id>', thread_detail, name='thread_detail')
    ]

app_name = "forum"
