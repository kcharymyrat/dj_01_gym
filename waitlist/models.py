from tkinter import CASCADE
from django.db import models

from django.conf import settings

from products.models import Product

User = settings.AUTH_USER_MODEL


class Waitlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField()

    def __str__(self) -> str:
        return f"{self.email} waits for {self.product.title}"
