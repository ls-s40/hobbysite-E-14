"""This file manages the views for the merchstore app."""

from django.views.generic import TemplateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseForbidden
from collections import defaultdict
from .models import Product, Transaction
from .forms import TransactionForm


class ProductListView(ListView):
    """Class-based view for the merchstore product list page."""

    model = Product
    template_name = 'merchstore/product_list.html'
    context_object_name = 'other_products'

    def get_context_data(self, **kwargs):
        """
        Customize context data for the view.

        This method adds information about products to the context
            depending on whether the user is authenticated or not.

        If the user is authenticated, the context will contain:
        - `user_products`:
            A queryset of products owned by the authenticated user.
        - `other_products`:
            A queryset of products that are not owned
                by the authenticated user.

        If the user is not authenticated, the context will contain:
        - `user_products`:
            Set to `None` since the user is not authenticated.
        - `other_products`:
            A queryset containing all products available.
        """
        context = super().get_context_data(**kwargs)

        user = self.request.user
        if user.is_authenticated:
            user_profile = user.profile
            context['user_products'] = Product.objects.filter(
                owner=user_profile
            )
            context['other_products'] = Product.objects.exclude(
                owner=user_profile
            )
        else:
            context['user_products'] = None
            context['other_products'] = Product.objects.all()

        return context


class ProductDetailView(DetailView):
    """Class-based view for the merchstore product detail page."""

    model = Product
    template_name = 'merchstore/product_detail.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        """Add extra context for transaction form and stock check."""
        context = super().get_context_data(**kwargs)
        product = context['product']

        # Add transaction form
        context['transaction_form'] = TransactionForm()

        # Check if current user is the owner
        context['is_owner'] = self.request.user.is_authenticated and (
            product.owner == self.request.user.profile
        )

        # Disable buy button if stock is 0
        context['disable_buy_button'] = product.stock == 0

        return context

    def post(self, request, *args, **kwargs):
        """Handle transaction form submission."""
        self.object = self.get_object()
        product = self.object
        form = TransactionForm(request.POST)

        if not request.user.is_authenticated:
            return redirect(f"{reverse_lazy('login')}?next={request.path}")

        if product.owner == request.user.profile:
            return HttpResponseForbidden("You cannot buy your own product.")

        if form.is_valid():
            amount = form.cleaned_data['amount']

            if product.stock < amount:
                form.add_error('amount', 'Not enough stock available.')
                return self.render_to_response(
                    self.get_context_data(transaction_form=form)
                )

            transaction = form.save(commit=False)
            transaction.buyer = request.user.profile
            transaction.product = product
            transaction.status = 'on_cart'
            transaction.save()

            # Update stock
            product.stock -= amount
            product.save()

            return redirect('merchstore:cart')
        else:
            return self.render_to_response(
                self.get_context_data(transaction_form=form)
            )


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
    ]
    success_url = reverse_lazy('merchstore:index')

    def form_valid(self, form):
        """Set owner to the logged-in user."""
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
    ]
    success_url = reverse_lazy('merchstore:index')

    def dispatch(self, request, *args, **kwargs):
        """Limits update access to Product owner."""
        product = self.get_object()
        if product.owner != request.user.profile:
            raise PermissionDenied(
                "You do not have permission to edit this product."
            )
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        """Set status based on stock."""
        if form.cleaned_data['stock'] == 0:
            form.instance.status = 'out_of_stock'
        else:
            form.instance.status = 'available'
        return super().form_valid(form)


class CartView(LoginRequiredMixin, TemplateView):
    """Shows all Transactions made by the logged-in user as the buyer."""

    template_name = 'merchstore/cart.html'

    def get_context_data(self, **kwargs):
        """
        Customize context data for the view.

        This method retrieves the transactions where the current user
            is the buyer and groups them by product owners.
        """
        context = super().get_context_data(**kwargs)
        user_profile = self.request.user.profile

        transactions = Transaction.objects.select_related(
            'product__owner').filter(buyer=user_profile)

        grouped_transactions = defaultdict(list)
        for tn in transactions:
            owner = tn.product.owner if tn.product else None
            grouped_transactions[owner].append(tn)

        context['grouped_transactions'] = dict(grouped_transactions)
        return context


class TransactionsListView(LoginRequiredMixin, TemplateView):
    """Shows all Transactions made by the logged-in user as the seller."""

    template_name = 'merchstore/transactions_list.html'

    def get_context_data(self, **kwargs):
        """
        Customize context data for the view.

        This method retrieves the transactions where the current user
            is the seller and groups them by product buyers.
        """
        context = super().get_context_data(**kwargs)
        user_profile = self.request.user.profile

        transactions = Transaction.objects.select_related(
            'product__owner', 'buyer').filter(product__owner=user_profile)

        grouped_transactions = defaultdict(list)
        for tn in transactions:
            buyer = tn.buyer
            grouped_transactions[buyer].append(tn)

        context['grouped_transactions'] = dict(grouped_transactions)
        return context
