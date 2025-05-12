"""This file manages the Models for the merchstore app."""

from django.db import models
from django.urls import reverse


class ProductType(models.Model):
    """Represents a ProductType Model."""

    name = models.CharField(max_length=255)
    description = models.TextField()

    class Meta:
        """Sorts ProductTypes by name in ascending order."""

        ordering = ['name']

    def __str__(self):
        """Presents ProductType instances as human-readable representations."""
        return self.name


class Product(models.Model):
    """Represents a Product Model."""

    PRODUCT_STATUS_CHOICES = [
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
        choices=PRODUCT_STATUS_CHOICES,
        default='available'
    )
    product_type = models.ForeignKey(
        ProductType,
        on_delete=models.SET_NULL,
        related_name='products',
        null=True,
        editable=False
    )
    owner = models.ForeignKey(
        'user_management.Profile',
        on_delete=models.CASCADE,
        related_name='products',
        null=True
    )

    def save(self, *args, **kwargs):
        """Set status to 'out_of_stock' when stock is 0."""
        if self.stock == 0:
            self.status = 'out_of_stock'
        super().save(*args, **kwargs)

    def __str__(self):
        """Presents ProductType instances as human-readable representations."""
        return self.name

    def get_absolute_url(self):
        """Return specific URL to view the instance."""
        return reverse('merchstore:product-detail', args=[str(self.id)])


class Transaction(models.Model):
    """Represents a Transaction Model."""

    TRANSACTION_STATUS_CHOICES = [
        ('on_cart', 'On cart'),
        ('to_pay', 'To Pay'),
        ('to_ship', 'To Ship'),
        ('to_receive', 'To Receive'),
        ('delivered', 'Delivered'),
    ]

    buyer = models.ForeignKey(
        'user_management.Profile',
        on_delete=models.SET_NULL,
        related_name='transactions',
        null=True
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.SET_NULL,
        related_name='transactions',
        null=True
    )
    amount = models.PositiveIntegerField(null=True)
    status = models.CharField(
        max_length=20,
        choices=TRANSACTION_STATUS_CHOICES,
    )
    created_on = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        """Presents Transaction instances as human-readable representations."""
        product_name = self.product.name if self.product else "Unknown Product"
        buyer_name = self.buyer.display_name if self.buyer else "Unknown Buyer"
        return f"{self.amount} x {product_name} by {buyer_name}"
