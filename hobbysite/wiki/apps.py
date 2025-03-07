"""Define app for project."""


from django.apps import AppConfig


class WikiConfig(AppConfig):
    """Configurate wiki app."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'wiki'
