from itertools import product
from django.db import models
import uuid


class Subscription(models.Model):
    email = models.CharField(max_length=255, unique=True)

class Product(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    description = models.TextField(default="")
    compare_at_price = models.DecimalField(max_digits=9, decimal_places=2)
    price = models.DecimalField(max_digits=9, decimal_places=2)
    colour = models.CharField(max_length=255, default="", null=True, blank=True)
    shopify_id = models.CharField(max_length=255)

    def __str__(self):
      return self.shopify_id


class ProductImage(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, editable=False)
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="images"
    )
    image = models.ImageField()


class ProductColour(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    hex_colour = models.CharField(max_length=255, null=True, blank=True)
    item = models.ForeignKey(Product, on_delete=models.CASCADE)


class CartSession(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, editable=False)
    session_id = models.CharField(max_length=255)
    expires_at = models.DateTimeField(null=True, blank=True)

class CartItem(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, editable=False)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    cart = models.ForeignKey(CartSession, on_delete=models.CASCADE, related_name="items")
    quantity = models.PositiveIntegerField(default=1)
    colour = models.CharField(max_length=255, null=True, blank=True)

class ContactSubmission(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=255)
    message = models.TextField()

