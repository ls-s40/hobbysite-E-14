"""Creates all pertinent models to be used in the forum app."""

from django.db import models
from django.utils.timezone import now
from django.urls import reverse

# Create your models here.


class PostCategory(models.Model):
    """Defines the PostCateogry model."""

    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        """Return PostCategory name."""
        return self.name

    def get_absolute_url(self):
        """Return absolute url of PostCategory."""
        return reverse('forum:thread_detail', args=[str(self.id)])


class Post(models.Model):
    """Defines the Post model."""

    title = models.CharField(max_length=255)
    category = models.ForeignKey(PostCategory,
                                on_delete=models.SET_NULL,
                                null=True)
    entry = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        """Return Post name."""
        return self.title

    def get_absolute_url(self):
        """Return absolute url of Post."""
        return reverse('forum:post_detail', args=[str(self.id)])
