from django import forms

from .models import Order


class OrderForm(forms.ModelForm):
    shipping_address = forms.CharField(
        label="", widget=forms.Textarea(attrs={"placeholder": "Shipping address"})
    )
    billing_address = forms.CharField(
        label="", widget=forms.Textarea(attrs={"placeholder": "Billing address"})
    )

    class Meta:
        model = Order
        fields = (
            "shipping_address",
            "billing_address",
        )
