#clarify if both of these are needed
from django.shortcuts import render
from django.http import HttpResponse

from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from .models import Product

class ProductListView(ListView):
    model = Product
    template_name = 'merchstore/product_list.html'

class ProductDetailView(DetailView):
    model = Product
    template_name = 'merchstore/product_detail.html'

