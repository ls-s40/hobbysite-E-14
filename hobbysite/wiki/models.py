from django.db import models
from django.utils.timezone import now
from django.urls import reverse

# Create your models here.
class ArticleCategory(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name

class Article(models.Model):

    title = models.CharField(max_length=255)
    category = models.ForeignKey(ArticleCategory, on_delete=models.SET_NULL, null=True)
    entry = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)  # Stores timestamp when record is created
    updated_on = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return reverse('wiki:article_detail', args=[str(self.id)])

    def __str__(self):
        return self.title
