from django.db import models
from django.conf import settings

from .storages import ProtectedStorage

User = settings.AUTH_USER_MODEL


class Product(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.TextField(null=True, blank=True)
    image = models.ImageField(null=True, blank=True, upload_to="products/")
    file = models.FileField(
        storage=ProtectedStorage, upload_to="products/", null=True, blank=True
    )
    price = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    inventory = models.IntegerField(default=0)
    is_featured = models.BooleanField(default=False)
    is_shippable = models.BooleanField(default=False)
    can_backorder = models.BooleanField(default=False)

    @property
    def has_digital(self):
        print("self.file =", self.file, self.file is None)
        return (not self.file is None) and (not self.file == "")

    def has_invetory(self):
        return self.inventory > 0

    def reduce_inventory(self, amount=1):
        initial_amount = self.inventory
        self.inventory = initial_amount - 1
        self.save()

    def __str__(self) -> str:
        return f"{self.title} - ${self.price}"
