"""This file is used to configure the accounts app."""
from django.apps import AppConfig


class AccountsConfig(AppConfig):
    """Configuration for accounts app."""
    
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'
