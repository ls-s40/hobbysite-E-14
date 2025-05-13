"""This file contains the forms for the user_management app."""
from django import forms
from .models import Profile


class ProfileForm(forms.ModelForm):
    """Form for creating and updating user profiles."""

    class Meta:
        """Meta class for ProfileForm."""

        model = Profile
        fields = ['display_name', 'email']
