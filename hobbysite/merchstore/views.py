"""This file manages the views for the merchstore app."""

from django.views.generic import TemplateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.core.exceptions import PermissionDenied
from collections import defaultdict
from .models import Product, Transaction
from .forms import TransactionForm


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

class ProductDetailView(LoginRequiredMixin, DetailView):
    """Class-based view for the merchstore product detail page."""

    model = Product
    template_name = 'merchstore/product_detail.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        """Adds extra context for transaction form and stock check."""
        context = super().get_context_data(**kwargs)
        product = context ['product']

        # Add transaction form
        context['transaction_form'] = TransactionForm()

        # Check if current user is the owner
        context['is_owner'] = product.owner == self.request.user.profile

        # Disable buy button if stock is 0
        context['disable_buy_button'] = product.stock == 0

        return context

    def post(self, request, *args, **kwargs):
        """Handles transaction form submission."""
        product = self.get_object()
        if product.owner == request.user.profile:
            messages.error(request, "You cannot purchase your own product.")
            return redirect('merchstore:product-detail', pk=product.pk)
        
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.buyer = request.user.profile
            transaction.product = product
            transaction.amount = form.cleaned_data['amount']
            
            # Update stock
            product.stock -= transaction.amount
            product.save()

            # Redirect according to login status
            if request.user.is_authenticated:
                transaction.save()
                return redirect('merchstore:cart')
            else:
                messages.info(request, "Please log in to complete your purchase.")
                return redirect('login')
        else:
            return render(request, 'merchstore/product-detail.html', {'product': product, 'transaction_form': form})


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


class CartView(LoginRequiredMixin, TemplateView):
    """Shows all Transactions made by the logged-in user."""
    template_name = 'merchstore/cart.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_profile = self.request.user.profile

        transactions = Transaction.objects.select_related('product__owner').filter(buyer=user_profile)

        grouped_transactions = defaultdict(list)
        for tn in transactions:
            owner = tn.product.owner if tn.product else None
            grouped_transactions[owner].append(tn)
        
        context['grouped_transactions'] = dict(grouped_transactions)
        return context
