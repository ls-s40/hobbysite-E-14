"""Creates all pertinent models to be used in the forum app."""

from django.db import models
from django.utils.timezone import now
from django.urls import reverse
from user_management.models import Profile

# Create your models here.


class ThreadCategory(models.Model):
    """Defines the ThreadCateogry model."""

    name = models.CharField(max_length=255)
    description = models.TextField()

    class Meta:
        ordering = ['name']

    def __str__(self):
        """Return PostCategory name."""
        return self.name

    def get_absolute_url(self):
        """Return absolute url of PostCategory."""
        return reverse('forum:thread_detail', args=[str(self.id)])


class Thread(models.Model):
    """Defines the Thread model."""

    title = models.CharField(max_length=255)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='thread_author' )
    category = models.ForeignKey(ThreadCategory,
                                on_delete=models.SET_NULL,
                                null=True)
    entry = models.TextField()
    image = models.ImageField(upload_to='forum/images/', blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        """Return Thread name."""
        return self.title

    def get_absolute_url(self):
        """Return absolute url of Thread."""
        return reverse('forum:thread_detail', args=[str(self.id)])
    

class Comment(models.Model):
    """Defines the Comment model."""

    author = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='comments')
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE, related_name='comments')
    entry = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        """Return the name of the commenter."""
        return self.author.display_name or self.author.user.username

    class Meta:
        """Meta options for the model."""

        ordering = ['-created_on']
