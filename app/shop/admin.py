from django.contrib import admin
from shop import models

# Register your models here.

@admin.register(models.Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
  list_display = ("email",)


admin.site.register(models.Product)
admin.site.register(models.CartSession)
admin.site.register(models.CartItem)
admin.site.register(models.ContactSubmission)
