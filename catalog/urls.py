from django.urls import path, include
from catalog.apps import CatalogConfig
from catalog.views import home, contact, product_about

app_name = CatalogConfig.name

urlpatterns = [
    path("", home, name="home"),
    path("contacts/", contact, name="contact"),
    path('product/<int:pk>', product_about, name='product_about')
]
