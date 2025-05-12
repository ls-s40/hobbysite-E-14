"""This file is used to configure the user_management app."""
from django.apps import AppConfig


class UserManagementConfig(AppConfig):
    """Configuration class for the user_management app."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'user_management'
