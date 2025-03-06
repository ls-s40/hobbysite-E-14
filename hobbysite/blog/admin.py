"""Admin interface for blog app."""
from django.contrib import admin
from .models import Article, ArticleCategory


class ArticleInline(admin.TabularInline):
    """Inline admin for Article model."""

    model = Article


class ArticleCategoryAdmin(admin.ModelAdmin):
    """Admin interface for managing ArticleCategory model."""

    list_display = ('name', 'description')
    search_fields = ('name',)


class ArticleAdmin(admin.ModelAdmin):
    """Admin interface for managing Article model."""

    list_display = ('title', 'category', 'created_on', 'updated_on')
    search_fields = ('title', 'entry')
    list_filter = ('category', 'created_on')
    ordering = ('-created_on',)


admin.site.register(Article, ArticleAdmin)
admin.site.register(ArticleCategory, ArticleCategoryAdmin)
