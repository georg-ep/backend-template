from django.urls import path

from shop import views

urlpatterns = [
    path("affiliate/fetch/", views.FetchAffiliateView.as_view(), name="fetch-affiliate"),
    path("affiliate/create/", views.CreateAffiliateView.as_view(), name="create-affiliate"),
    path("product/<str:slug>/", views.ProductDetailView.as_view(), name="detail"),
    path("fetch_cart/", views.CartView.as_view(), name="cart"),
    path("line_items/update/", views.update_line_items),
    path("contact/submission/", views.CreateContactSubmissionView.as_view()),
    path("subscribe/", views.SubscribeView.as_view(), name="subscribe"),
]
