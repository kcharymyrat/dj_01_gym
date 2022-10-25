from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()


class RegisterForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
            }
        )
    )
    email = forms.CharField(
        widget=forms.EmailInput(
            attrs={
                "class": "form-control",
            }
        )
    )
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
            }
        ),
    )
    password2 = forms.CharField(
        label="Confirm your password",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
            }
        ),
    )

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")
        if password1 != password2:
            raise forms.ValidationError("Passwords don't match")

    def clean_username(self):
        username = self.cleaned_data.get("username")
        qs = User.objects.filter(username__iexact=username)
        if qs.exists():
            raise forms.ValidationError("This is invalid username, try another one")
        return username

    def clean_email(self):
        email = self.cleaned_data.get("email")
        qs = User.objects.filter(email__iexact=email)
        if qs.exists():
            raise forms.ValidationError("This email is already on use, try another one")
        return email


class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "id": "password",
            }
        )
    )

    def clean_username(self):
        username = self.cleaned_data.get("username")
        qs = User.objects.filter(username__iexact=username)
        if not qs.exists():
            raise forms.ValidationError("This is an invalid username")
        return username
