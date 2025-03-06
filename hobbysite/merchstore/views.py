"""This file manages the views for the merchstore app."""

from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from .models import Product


class ProductListView(ListView):
    """Class-based view for the merchstore product list page."""

    model = Product
    template_name = 'merchstore/product_list.html'


class ProductDetailView(DetailView):
    """Class-based view for the merchstore product detail page."""

    model = Product
    template_name = 'merchstore/product_detail.html'
