from django import forms
from .models import Transaction

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['amount']
    
    amount = forms.IntegerField(min_value=1, label="Quantity")
