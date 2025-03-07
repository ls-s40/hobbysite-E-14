"""Admin site is created here."""

from django.contrib import admin
from .models import Article, ArticleCategory


class ArticleAdmin(admin.ModelAdmin):
    """Registers article model as model to be used for admin page."""

    model = Article


class ArticleCategoryAdmin(admin.ModelAdmin):
    """Registers article category model as model to be used for admin page."""

    model = ArticleCategory


admin.site.register(Article, ArticleAdmin)
admin.site.register(ArticleCategory, ArticleCategoryAdmin)
