from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView

from catalog.forms import ProductForm, VersionForm
from catalog.models import Product, Version
from django.urls import reverse_lazy
from django.forms import inlineformset_factory


class ProductListView(ListView):
    """
    Контроллер перечня товаров
    """
    model = Product

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        for product in context_data['object_list']:
            actual_version = Version.objects.filter(product=product, is_actual=True).first()
            product.actual_version = actual_version

        return context_data


def contact(request):
    """
    Контроллер страницы с контактами
    """
    if request.method == "POST":
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        message = request.POST.get("message")
        print(f"You have new message from {name}({phone}): {message}")
    return render(request, "catalog/contact.html")


class ProductDetailView(DetailView):
    """
    Контроллер детального отображения товара
    """
    model = Product


class ProductCreateView(CreateView):
    """
    Контроллер создания товара
    """
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('catalog:home')
