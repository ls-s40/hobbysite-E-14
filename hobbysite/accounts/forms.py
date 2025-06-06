"""This file containts the forms for the accounts app."""
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class RegisterForm(UserCreationForm):
    """A form for creating new users."""

    display_name = forms.CharField(max_length=63, required=True)

    class Meta:
        """Meta class for RegisterForm."""
        
        model = User
        fields = (
            'username',
            'email',
            'password1',
            'password2',
            'display_name'
            )
