from django.urls import path

from . import views

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("about/", views.AboutView.as_view(), name="about"),
    path("products/", views.ProductListView.as_view(), name="products"),
    path(
        "products/<int:pk>/",
        views.ProductDetailView.as_view(),
        name="product-detail",
    ),
    path(
        "products/<int:product_pk>/add-to-cart/",
        views.AddToCartView.as_view(),
        name="add-to-cart",
    ),
    path("cart/", views.CartView.as_view(), name="cart"),
    path(
        "cart/<int:cart_item_pk>/delete/",
        views.CartDeleteView.as_view(),
        name="cart-delete",
    ),
]
