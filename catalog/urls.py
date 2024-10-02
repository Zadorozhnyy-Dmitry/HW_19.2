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
from django.views.decorators.cache import cache_page


app_name = CatalogConfig.name

urlpatterns = [
    path("", ProductListView.as_view(), name="home"),
    path("contacts/", contact, name="contact"),
    path(
        "product/<int:pk>/",
        cache_page(60)(ProductDetailView.as_view()),
        name="product_about",
    ),
    path("create/", ProductCreateView.as_view(), name="create_product"),
    path("edit/<int:pk>/", ProductUpdateView.as_view(), name="update_product"),
    path("delete/<int:pk>/", ProductDeleteView.as_view(), name="delete_product"),
]
