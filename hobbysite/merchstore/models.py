"""This file manages the Models for the merchstore app."""

from django.db import models
from django.urls import reverse


class ProductType(models.Model):
    """Represents a ProductType Model."""

    name = models.CharField(max_length=255)
    description = models.TextField()

    class Meta:
        ordering = ['name']
    
    def __str__(self):
        """Presents ProductType instances as human-readable representations."""
        return self.name


class Product(models.Model):
    """Represents a Product Model."""

    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    product_type = models.ForeignKey(
        ProductType,
        on_delete=models.SET_NULL,
        null=True,
        related_name='products'
    )

    def __str__(self):
        """Presents ProductType instances as human-readable representations."""
        return self.name

    def get_absolute_url(self):
        """Return specific URL to view the instance."""
        return reverse('merchstore:product-detail', args=[str(self.id)])
