"""This file manages admin panels for the forum app."""

from django.contrib import admin
from .models import Thread, ThreadCategory

# Register your models here.


class ThreadAdmin(admin.ModelAdmin):
    """Creates admin panel for Post model."""

    model = Thread


class ThreadCategoryAdmin(admin.ModelAdmin):
    """Creates admin panel for PostCategory model."""

    model = ThreadCategory


admin.site.register(Thread, ThreadAdmin)
admin.site.register(ThreadCategory, ThreadCategoryAdmin)
