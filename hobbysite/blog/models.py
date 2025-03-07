"""This module contains the models for the blog app."""
from django.db import models
from django.urls import reverse


class ArticleCategory(models.Model):
    """Model for article categories."""

    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        """Return the name of the category."""
        return self.name

    class Meta:
        """Meta options for the model."""

        ordering = ['name']
        verbose_name_plural = 'Article Categories'
        verbose_name = 'Article Category'


class Article(models.Model):
    """Model for articles."""

    title = models.CharField(max_length=255)
    category = models.ForeignKey(
        ArticleCategory,
        on_delete=models.SET_NULL,
        null=True, related_name='articles')
    entry = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        """Return the title of the article."""
        return self.title

    def get_absolute_url(self):
        """Return the URL for the article detail view."""
        return reverse('article_detail', args=[self.id])

    class Meta:
        """Meta options for the model."""

        ordering = ['-created_on']
