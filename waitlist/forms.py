from dataclasses import fields
from pyexpat import model
from socket import fromshare
from django import forms

from .models import Waitlist


class WaitlistModelForm(forms.ModelForm):
    class Meta:
        model = Waitlist
        fields = ("first_name", "last_name", "email")
