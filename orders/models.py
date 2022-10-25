from decimal import Decimal

from django.db import models
from django.conf import settings
from django.db.models.signals import pre_save, post_save

from products.models import Product

User = settings.AUTH_USER_MODEL




class Order(models.Model):
    ORDER_STATUS = (
        ('created', 'Created'),
        ('stale', 'Stale'),
        ('paid', 'Paid'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    subtotal = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
    tax = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
    total = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
    paid = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
    status = models.CharField(max_length=100, choices=ORDER_STATUS, default='created')
    shipping_address = models.TextField(blank=True, null=True)
    billing_address = models.TextField(blank=True, null=True)
    is_inventory_updated = models.BooleanField(default=False)

    def mark_paid(self):
        self.paid = self.total
        self.status = 'paid'
        self.save()

    def update_inventory(self, amount=1):
        self.product.reduce_inventory(amount)
        self.is_inventory_updated = True
        self.save()

    def calculate(self):
        subtotal = self.product.price
        tax_rate = Decimal(0.15).quantize(Decimal('.01'))
        tax = Decimal(subtotal * tax_rate).quantize(Decimal('.01')) 
        total = Decimal(subtotal+tax).quantize(Decimal('.01'))
        totals = {
            'subtotal': subtotal,
            'tax': tax,
            'total': total,
        }
        for k,v in totals.items():
            setattr(self, k, v)

    def __str__(self) -> str:
        return f"Order {self.id} by {self.user}: {self.product} for {self.total}"


def calculate_totals(sender, instance, **kwargs):
    instance.calculate()

pre_save.connect(calculate_totals, sender=Order)


