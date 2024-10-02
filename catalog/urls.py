from django.urls import path, include
from catalog.apps import CatalogConfig
from catalog.views import (
    contact,
    ProductListView,
    ProductDetailView,
    ProductCreateView,
    ProductUpdateView,
    ProductDeleteView,
)
from django.views.decorators.cache import cache_page, never_cache


app_name = CatalogConfig.name

urlpatterns = [
    path("", ProductListView.as_view(), name="home"),
    path("contacts/", contact, name="contact"),
    path(
        "product/<int:pk>/",
        cache_page(60)(ProductDetailView.as_view()),
        name="product_about",
    ),
    path("create/", never_cache(ProductCreateView.as_view()), name="create_product"),
    path(
        "edit/<int:pk>/",
        never_cache(ProductUpdateView.as_view()),
        name="update_product",
    ),
    path("delete/<int:pk>/", ProductDeleteView.as_view(), name="delete_product"),
]
