"""This file manages the views for the merchstore app."""

from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.core.exceptions import PermissionDenied
from .models import Product


class ProductListView(LoginRequiredMixin, ListView):
    """Class-based view for the merchstore product list page."""

    model = Product
    template_name = 'merchstore/product_list.html'
    context_object_name = 'other_products'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_profile = self.request.user.profile

        # Products owned by user
        context['user_products'] = Product.objects.filter(owner=user_profile)

        # Products NOT owned by user
        context['other_products'] = Product.objects.exclude(owner=user_profile)

        return context

class ProductDetailView(DetailView):
    """Class-based view for the merchstore product detail page."""

    model = Product
    template_name = 'merchstore/product_detail.html'

class ProductCreateView(LoginRequiredMixin, CreateView):
    """Allows logged-in users to create a new Product."""

    model = Product
    template_name = 'merchstore/product_form.html'
    fields = [
        'name',
        'description',
        'price',
        'stock',
        'status',
        'product_type'
    ]
    success_url = reverse_lazy('merchstore:index')

    def form_valid(self, form):
        """Sets owner to the logged-in user."""
        form.instance.owner = self.request.user.profile
        return super().form_valid(form)

class ProductUpdateView(LoginRequiredMixin, UpdateView):
    """Allows logged-in users to update a Product."""

    model = Product
    template_name = 'merchstore/product_form.html'
    fields = [
        'name',
        'description',
        'price',
        'stock',
        'status',
        'product_type'
    ]
    success_url = reverse_lazy('merchstore:index')

    def dispatch(self, request, *args, **kwargs):
        """Limits update access to Product owner."""
        product = self.get_object()
        if product.owner != request.user.profile:
            raise PermissionDenied("You do not have permission to edit this product.")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        """Sets status based on stock."""
        if form.cleaned_date['stock'] == 0:
            form.instance.status = 'out_of_stock'
        else:
            form.instance.status = 'available'
        return super().form_valid(form)
