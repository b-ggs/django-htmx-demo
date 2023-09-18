from django.contrib.postgres.fields import ArrayField
from django.db import models

from htmx_demo.users.models import User


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    variants = ArrayField(models.CharField(max_length=255), blank=True)
    price_cents = models.PositiveIntegerField()
    image_url = models.URLField(default="https://placehold.co/600x400")

    @property
    def price(self) -> float:
        return self.price_cents / 100

    def __str__(self) -> str:
        return self.name


class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    variant = models.CharField(max_length=255, blank=True)

    @property
    def price(self) -> float:
        return self.product.price * self.quantity

    def __str__(self) -> str:
        return f"{self.product} ({self.quantity})"
