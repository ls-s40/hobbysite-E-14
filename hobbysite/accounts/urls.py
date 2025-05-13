"""This file contains the URL patterns for the accounts app."""
from django.urls import path
from .views import register_view

urlpatterns = [
    path('register/', register_view, name='register'),
]

app_name = 'accounts'
