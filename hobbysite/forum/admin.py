"""This file manages admin panels for the forum app."""

from django.contrib import admin
from .models import Post, PostCategory

# Register your models here.


class PostAdmin(admin.ModelAdmin):
    """Creates admin panel for Post model."""

    model = Post


class PostCategoryAdmin(admin.ModelAdmin):
    """Creates admin panel for PostCategory model."""

    model = PostCategory


admin.site.register(Post, PostAdmin)
admin.site.register(PostCategory, PostCategoryAdmin)
