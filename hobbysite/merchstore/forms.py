"""This file manages the Forms for the merchstore app."""

from django import forms
from .models import Transaction


class TransactionForm(forms.ModelForm):
    """Django form for the Transaction Model."""

    class Meta:
        """Specifies the Transaction Model and the amount field."""

        model = Transaction
        fields = ['amount']

    amount = forms.IntegerField(min_value=1, label="Quantity")
