from math import prod
from django.shortcuts import render
from shop.models import Affiliate
from rest_framework import generics
from shop.models import Product
from shop import serializers
from rest_framework.decorators import api_view
from rest_framework.response import Response

import json
from shop.models import CartSession, CartItem, Product
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Sum
from shop.serializers import CartSerializer
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response

class CreateAffiliateView(generics.CreateAPIView):
    serializer_class = serializers.CreateAffiliateSerializer

class FetchAffiliateView(generics.RetrieveAPIView):
    serializer_class = serializers.FetchAffiliateSerializer

class SubscribeView(generics.CreateAPIView):
    serializer_class = serializers.SubscribeSerializer

class CreateContactSubmissionView(generics.CreateAPIView):
    serializer_class = serializers.CreateContactSubmissionSerializer

class ProductDetailView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = serializers.ProductDetailSerializer
    lookup_url_kwarg = "slug"
    lookup_field = "slug"

class ProductListView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = serializers.ProductListSerializer


def fetch_session(request):
    if not request.session.session_key:
        request.session.create()
    return request.session.session_key


class CartView(generics.RetrieveAPIView):
    serializer_class = CartSerializer
    queryset = CartSession.objects.all()

    def get_object(self):
        print(self.request.session.__dict__)
        session = fetch_session(self.request)
        return super().get_queryset().filter(session_id=session).first()


def update_cart(cart, data, product, colour, action):

    def add(item, quantity):
      item.quantity += quantity

    def setq(item, quantity):
      if quantity == 0:
        item.delete()
        print("deleted", item)
      else:
        item.quantity = quantity
        item.save()
      # item.quantity = quantity if quantity > 0 else item.delete()


    query = Q(product=product) & Q(colour=colour)

    if cart.items.filter(query).exists():
        item = cart.items.get(query)
        config = {
          "add": add(item, data["quantity"]),
          "set": setq(item, data["quantity"]),
        }

        config[action]
        
    else:
        CartItem.objects.create(
            quantity=data["quantity"],
            colour=colour,
            product=product,
            cart=cart,
        )


@csrf_exempt
@api_view(["POST"])
def update_line_items(request):
    try:
        data = json.loads(request.body)
    except Exception:
        print("Error whilst parsing body")

    session = fetch_session(request)

    if "product_id" in data:
        colour = None
        action = "add"

        if "colour" in data:
            colour = data["colour"]

        if "action" in data:
            action = data["action"]

        cart, created = CartSession.objects.get_or_create(session_id=session)

        try:
            product = Product.objects.get(shopify_id=data["product_id"])
        except Exception:
            print("error finding product")
            return Response({"status": "fail"})

        update_cart(cart, data, product, colour, action)

        serializer = CartSerializer(cart)

        return Response(serializer.data)
    return Response({"status": "fail"})
