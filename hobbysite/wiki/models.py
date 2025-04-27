"""Models for the wiki are made here."""

from django.db import models
from django.urls import reverse


class ArticleCategory(models.Model):
    """Creates model for ArticleCategory."""

    name = models.CharField(max_length=255)
    description = models.TextField()

    class Meta:
        ordering = ['name']
    
    def __str__(self):
        """Return string name when asked to print object."""
        return self.name


class Article(models.Model):
    """Creates model for Article."""

    title = models.CharField(max_length=255)
    category = models.ForeignKey(
        ArticleCategory,
        on_delete=models.SET_NULL,
        null=True
    )
    entry = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        """Return URL of wiki article by id."""
        return reverse('wiki:article_detail', args=[str(self.id)])

    def __str__(self):
        """Return string name when asked to print object."""
        return self.title
