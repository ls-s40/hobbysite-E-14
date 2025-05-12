"""Models for the wiki are defined here."""

from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


class ArticleCategory(models.Model):
    """Model for article categories."""

    name = models.CharField(max_length=255)
    description = models.TextField()

    class Meta:
        """Metadata for ArticleCategory."""

        ordering = ['name']

    def __str__(self):
        """Return the name of the category."""
        return self.name


class Article(models.Model):
    """Model for wiki articles."""

    title = models.CharField(max_length=255)
    author = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True
    )
    category = models.ForeignKey(
        ArticleCategory,
        on_delete=models.SET_NULL,
        null=True
    )
    entry = models.TextField()
    header_image = models.ImageField(
        upload_to='wiki/images/',
        blank=True,
        null=True
    )
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        """Return the URL of the article."""
        return reverse('wiki:article_detail', args=[str(self.id)])

    def __str__(self):
        """Return the title of the article."""
        return self.title

    class Meta:
        """Metadata for Article."""

        ordering = ['-created_on']


class Comment(models.Model):
    """Model for comments on articles."""

    author = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True
    )
    article = models.ForeignKey(
        Article,
        on_delete=models.CASCADE,
    )
    entry = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        """Metadata for Comment."""

        ordering = ['-created_on']
