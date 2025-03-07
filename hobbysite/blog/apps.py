"""This file is used to configure the blog app."""
from django.apps import AppConfig


class BlogConfig(AppConfig):
    """Configuration for blog app."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'blog'
