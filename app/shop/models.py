from distutils.command.upload import upload
from django.db import models
import uuid
from core.models import safe_file_path


class Subscription(models.Model):
    email = models.CharField(max_length=255, unique=True)


class Product(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    description = models.TextField(default="", null=True, blank=True)
    compare_at_price = models.DecimalField(max_digits=9, decimal_places=2)
    price = models.DecimalField(max_digits=9, decimal_places=2)
    shopify_id = models.CharField(max_length=255, editable=False)
    slug = models.CharField(max_length=255, default="", unique=True)

    def __str__(self):
        return self.name


class Review(models.Model):
    name = models.CharField(max_length=255)
    stars = models.PositiveSmallIntegerField()
    image = models.FileField(upload_to=safe_file_path, null=True, blank=True)
    description = models.TextField(null=True, blank=True, default="")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="reviews")
    item_type = models.CharField(max_length=255, default="")

    def __str__(self):
      return f"Review by: {self.name} - {self.stars}/5"

class ProductSection(models.Model):
    title = models.TextField()
    file = models.FileField(upload_to=safe_file_path, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="sections")
    content = models.TextField()

class ProductImage(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, editable=False)
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="images"
    )
    image = models.FileField(upload_to=safe_file_path)


class ProductColour(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    hex_colour = models.CharField(max_length=255, null=True, blank=True)
    item = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="colours")


class CartSession(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, editable=False)
    session_id = models.CharField(max_length=255)
    expires_at = models.DateTimeField(null=True, blank=True)


class CartItem(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, editable=False)
    product = models.ForeignKey(
        Product, on_delete=models.SET_NULL, null=True, blank=True
    )
    cart = models.ForeignKey(
        CartSession, on_delete=models.CASCADE, related_name="items"
    )
    quantity = models.PositiveIntegerField(default=1)
    colour = models.CharField(max_length=255, null=True, blank=True)


class ContactSubmission(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=255)
    message = models.TextField()
