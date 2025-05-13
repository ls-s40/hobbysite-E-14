"""This file containts the models for the user_management app."""
from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    """This model represents a user profile."""

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    display_name = models.CharField(max_length=63)
    email = models.EmailField()

    def __str__(self):
        """Return string of the Profile model."""
        return self.display_name or self.user.username
