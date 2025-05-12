"""This file manages the URLs for the merchstore app."""

from django.urls import path
from .views import ProductListView, ProductDetailView, ProductCreateView, ProductUpdateView, CartView

urlpatterns = [
    path('items/', ProductListView.as_view(), name='index'),
    path('item/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
    path('item/add/', ProductCreateView.as_view(), name='product-create'),
    path('item/<int:pk>/edit/', ProductUpdateView.as_view(), name='product-edit'),
    path('cart/', CartView.as_view(), name='cart'),
]

app_name = "merchstore"
