from django.urls import path, include
from catalog.apps import CatalogConfig
from catalog.views import contact, ProductListView, ProductDetailView

app_name = CatalogConfig.name

urlpatterns = [
    path("", ProductListView.as_view(), name="home"),
    path("contacts/", contact, name="contact"),
    path("product/<int:pk>", ProductDetailView.as_view(), name="product_about"),
]
