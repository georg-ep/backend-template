from django.contrib import admin
from shop import models

# Register your models here.

@admin.register(models.Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
  list_display = ("email",)

class ProductColourInline(admin.StackedInline):
  extra = 0
  model = models.ProductColour

class ProductImageInline(admin.StackedInline):
  extra = 0
  model = models.ProductImage

class ProductSectionInline(admin.StackedInline):
  extra = 0
  model = models.ProductSection

@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
  list_display = ("name", "uid", "shopify_id", "price",)
  inlines = [ProductColourInline, ProductImageInline, ProductSectionInline]
  readonly_fields = ["uid", "shopify_id"]

@admin.register(models.Review)
class ReviewAdmin(admin.ModelAdmin):
  list_display = ("__str__", "product",)

@admin.register(models.Affiliate)
class AffiliateAdmin(admin.ModelAdmin):
  list_display = ("first_name", "last_name", "email", "code",)

admin.site.register(models.CartSession)
admin.site.register(models.CartItem)
admin.site.register(models.ContactSubmission)
