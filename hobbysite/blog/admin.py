"""Admin interface for blog app."""
from django.contrib import admin
from .models import Article, ArticleCategory, Comment


class ArticleInline(admin.TabularInline):
    """Inline admin for Article model."""

    model = Article
    extra = 1


class ArticleCategoryAdmin(admin.ModelAdmin):
    """Admin interface for managing ArticleCategory model."""

    list_display = ('name', 'description')
    search_fields = ('name',)
    inlines = [ArticleInline]


class CommentAdmin(admin.ModelAdmin):
    """Admin interface for managing Comment model."""

    list_display = ('author', 'article', 'entry', 'created_on', 'updated_on')
    search_fields = ('entry', 'author__user__username', 'article__title')
    list_filter = ('created_on', 'updated_on', 'article')
    ordering = ('-created_on',)


class CommentInline(admin.TabularInline):
    """Inline admin for Comment model."""

    model = Comment
    extra = 1


class ArticleAdmin(admin.ModelAdmin):
    """Admin interface for managing Article model."""

    list_display = ('title', 'category', 'created_on', 'updated_on')
    search_fields = (
        'title',
        'entry',
        'author__user__username',
        'category__name'
        )
    list_filter = ('category', 'created_on', 'updated_on')
    ordering = ('-created_on',)
    readonly_fields = ('created_on', 'updated_on')
    inlines = [CommentInline]


admin.site.register(Article, ArticleAdmin)
admin.site.register(ArticleCategory, ArticleCategoryAdmin)
admin.site.register(Comment, CommentAdmin)
