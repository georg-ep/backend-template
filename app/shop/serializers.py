from rest_framework import serializers
from shop.models import Product, CartSession, CartItem, ContactSubmission, Subscription
from django.db.models import F, Sum

class SubscribeSerializer(serializers.ModelSerializer):
    class Meta:
      model = Subscription
      fields = ("email",)

class CreateContactSubmissionSerializer(serializers.ModelSerializer):
    class Meta:
      model = ContactSubmission
      fields = "__all__"

class ProductDetailSerializer(serializers.ModelSerializer):
    class Meta:
      model = Product
      fields = "__all__"

class CartItemSerializer(serializers.ModelSerializer):
    product = ProductDetailSerializer()

    class Meta:
        model = CartItem
        fields = "__all__"

class CartSerializer(serializers.ModelSerializer):
    line_items = CartItemSerializer(many=True, source="items")
    total = serializers.SerializerMethodField()
    total_cart_items = serializers.SerializerMethodField()

    def get_total_cart_items(self, obj):
        query = Sum("items__quantity")
        cart = CartSession.objects.annotate(total_cart_items=query).get(id=obj.id)
        return cart.total_cart_items

    def get_total(self, obj):
        query = Sum(F("items__product__price") * F("items__quantity"))
        cart = CartSession.objects.annotate(total=query).get(id=obj.id)
        return cart.total

    class Meta:
      model = CartSession
      fields = ("line_items", "total", "total_cart_items",)
