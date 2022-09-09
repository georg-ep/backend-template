from rest_framework import serializers
from shop.models import Product, CartSession, CartItem, ContactSubmission, Subscription, Review, ProductSection, ProductImage, ProductColour, Affiliate
from django.db.models import F, Sum, Avg
import secrets

class SubscribeSerializer(serializers.ModelSerializer):
    class Meta:
      model = Subscription
      fields = ("email",)

class CreateContactSubmissionSerializer(serializers.ModelSerializer):
    class Meta:
      model = ContactSubmission
      fields =  ("email", "name", "message",)

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
      model = Review
      exclude = ("product", "id",)

class SectionSerializer(serializers.ModelSerializer):
    class Meta:
      model = ProductSection
      exclude = ("product", "id",)

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
      model = ProductImage
      exclude = ("product", "id", "uid",)

class ProductColourSerializer(serializers.ModelSerializer):
    class Meta:
      model = ProductColour
      exclude = ("id", "item", "uid",)

class ProductDetailSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True)
    sections = SectionSerializer(many=True)
    images = ProductImageSerializer(many=True)
    colours = ProductColourSerializer(many=True)

    average_rating = serializers.SerializerMethodField()
    reduction_perc = serializers.SerializerMethodField()

    class Meta:
      model = Product
      exclude = ("id",)
    
    def get_reduction_perc(self, obj):
      price = obj.price
      compare = obj.compare_at_price
      return (price * 100 / compare) if compare else None

    def get_average_rating(self, obj):
      return obj.reviews.aggregate(average=Avg("stars"))['average']

class ProductListSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True)
    average_rating = serializers.SerializerMethodField()
    reduction_perc = serializers.SerializerMethodField()

    class Meta:
      model = Product
      exclude = ("id",)
    
    def get_reduction_perc(self, obj):
      price = obj.price
      compare = obj.compare_at_price
      return (price * 100 / compare) if compare else None

    def get_average_rating(self, obj):
      return obj.reviews.aggregate(average=Avg("stars"))['average']

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

class CreateAffiliateSerializer(serializers.ModelSerializer):
    
    def create(self, validated_data):
      instance = super().create(validated_data)

      id_s = str(instance.id)
      upper_alpha = "ABCDEFGHJKLMNPQRSTVWXYZ"
      random_str = "".join(secrets.choice(upper_alpha) for i in range(8))
      instance.code = (random_str + id_s)[-8:]
      instance.save()

      return instance

    class Meta:
      model = Affiliate
      fields = ("email", "first_name", "last_name", "code",)

class FetchAffiliateSerializer(serializers.ModelSerializer):
    class Meta:
      model = Affiliate
      fields = ("email",)