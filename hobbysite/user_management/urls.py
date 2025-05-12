"""This file contains the URL patterns for the accounts app."""
from django.urls import path
from .views import profile_update_view

urlpatterns = [
    path('<str:username>/', profile_update_view, name='profile_update')
]

app_name = 'user_management'