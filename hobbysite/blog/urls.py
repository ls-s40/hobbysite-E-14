"""This file contains the URL patterns for the blog app."""
from django.urls import path
from .views import article_list, article_detail, article_create, article_update

urlpatterns = [
    path('articles/', article_list, name='index'),
    path('article/<int:id>/', article_detail, name='article_detail'),
    path('article/add/', article_create, name='article_create'),
    path('article/<int:id>/edit', article_update, name='article_update'),
]

app_name = 'blog'
