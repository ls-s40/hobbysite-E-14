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

    STATUS_CHOICES=[
        ('available', 'Available'),
        ('on_sale', 'On sale'),
        ('out_of_stock', 'Out of stock'),
    ]

    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(null=True)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='available'
    )
    product_type = models.ForeignKey(
        ProductType,
        on_delete=models.SET_NULL,
        null=True,
        related_name='products',
        editable=False
    )
    owner=models.ForeignKey(
        'user_management.Profile',
        on_delete=models.CASCADE,
        related_name='products',
        null=True
    )

    def save(self, *args, **kwargs):
        """Sets status to 'out_of_stock' when stock is 0."""
        if self.stock == 0:
            self.status = 'out_of_stock'
        super().save(*args, **kwargs)

    def __str__(self):
        """Presents ProductType instances as human-readable representations."""
        return self.name

    def get_absolute_url(self):
        """Return specific URL to view the instance."""
        return reverse('merchstore:product-detail', args=[str(self.id)])
