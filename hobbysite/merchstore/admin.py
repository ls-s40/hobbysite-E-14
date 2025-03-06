"""This file manages the admin panels for the merchstore app."""

from django.contrib import admin
from .models import ProductType, Product


class ProductTypeAdmin(admin.ModelAdmin):
    """Handles admin for ProductType Model."""

    model = ProductType
    ordering = ['name']


class ProductAdmin(admin.ModelAdmin):
    """Handles admin for Product Model."""

    model = Product
    ordering = ['name']


admin.site.register(ProductType, ProductTypeAdmin)
admin.site.register(Product, ProductAdmin)
