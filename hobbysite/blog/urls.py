"""This file contains the URL patterns for the blog app."""
from django.urls import path
from .views import article_list, article_detail

urlpatterns = [
    path('blog/articles/', article_list, name='article_list'),
    path('blog/article/<int:id>/', article_detail, name='article_detail'),
]

app_name = 'blog'
