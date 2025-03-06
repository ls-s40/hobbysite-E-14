"""Admin config for Commission and Comment"""

from django.contrib import admin
from .models import Commission, Comment


class CommentInline(admin.TabularInline):
    """Inline admin for comments"""
    model = Comment


class CommissionAdmin(admin.ModelAdmin):
    """Admin for Commission"""
    model = Commission
    inlines = [CommentInline]


class CommentAdmin(admin.ModelAdmin):
    """Admin for Comment model"""
    model = Comment


admin.site.register(Commission, CommissionAdmin)
admin.site.register(Comment, CommentAdmin)
