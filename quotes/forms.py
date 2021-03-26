from django import forms
from .models import stock

class StockForm(forms.ModelForm):
    class Meta:
        model = stock
        fields = ["symbol"]