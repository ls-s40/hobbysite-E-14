from django.contrib import admin
from .models import ProductType, Product

class ProductTypeAdmin(admin.ModelAdmin):
    model = ProductType
    ordering = ['name']

class ProductAdmin(admin.ModelAdmin):
    model = Product
    ordering = ['name']

admin.site.register(ProductType, ProductTypeAdmin)
admin.site.register(Product, ProductAdmin)
