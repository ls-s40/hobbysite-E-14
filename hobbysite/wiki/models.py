"""Models for the wiki are made here."""

from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


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
    header_image = models.ImageField(upload_to='wiki/images/', blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        """Return URL of wiki article by id."""
        return reverse('wiki:article_detail', args=[str(self.id)])

    def __str__(self):
        """Return string name when asked to print object."""
        return self.title
    
    class Meta:
        ordering = ['-created_on']

class Comment(models.Model):
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
        ordering = ['-created_on']
