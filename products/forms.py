from django import forms

from .models import Product


class ProductForm(forms.Form):
    title = forms.CharField(max_length=100)
    # content = forms.CharField(widget=forms.Textarea)
    price = forms.DecimalField(max_digits=9, decimal_places=2)


class ProductModelForm(forms.ModelForm):
    title = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
            }
        )
    )

    class Meta:
        model = Product
        fields = ("title", "price", "image", "file")

    def clean_title(self):
        title = self.cleaned_data.get("title")
        if len(title) < 4:
            raise forms.ValidationError("Title must be minimum 4 characters long")
        return title
