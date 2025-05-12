"""This file contains admin configurations for the user_management app."""
from django.contrib import admin
from .models import Profile


class ProfileAdmin(admin.ModelAdmin):
    """Admin interface for managing Profile model."""

    list_display = ('user', 'display_name', 'email')
    search_fields = ('user__username', 'display_name', 'email')
    list_filter = ('user__is_active',)
    ordering = ('user__username',)


admin.site.register(Profile, ProfileAdmin)
