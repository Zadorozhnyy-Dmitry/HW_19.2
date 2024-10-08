from django.shortcuts import render, get_object_or_404
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)

from catalog.forms import ProductForm, VersionForm, ProductModeratorForm
from catalog.models import Product, Version, Category
from django.urls import reverse_lazy
from django.forms import inlineformset_factory
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied

from catalog.services import get_objects_from_cache


class ProductListView(ListView):
    """
    Контроллер перечня товаров
    """

    model = Product

    def get_context_data(self, **kwargs):
        """
        Расширяем данные информацией по актуальной версии товара
        """
        context_data = super().get_context_data(**kwargs)
        for product in context_data["object_list"]:
            actual_version = Version.objects.filter(
                product=product, is_actual=True
            ).first()
            product.actual_version = actual_version

        return context_data

    def get_queryset(self):
        """
        Вызов сервисной функции, для кэширования
        """
        return get_objects_from_cache(Product)


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


class ProductDetailView(LoginRequiredMixin, DetailView):
    """
    Контроллер детального отображения товара
    """

    model = Product

    def get_object(self, queryset=None):
        """
        Только владелец может просматривать карточук товара
        """
        self.object = super().get_object(queryset)
        if self.request.user == self.object.owner:
            return self.object
        raise PermissionDenied


class ProductCreateView(LoginRequiredMixin, CreateView):
    """
    Контроллер создания товара
    """

    model = Product
    form_class = ProductForm
    success_url = reverse_lazy("catalog:home")

    def form_valid(self, form):
        """
        Автоматическая привязка пользователя к продукту
        """
        product = form.save()
        user = self.request.user
        product.owner = user
        product.save()
        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    """
    Контроллер обновления товара
    """

    model = Product
    form_class = ProductForm
    success_url = reverse_lazy("catalog:home")

    def get_context_data(self, **kwargs):
        """
        Добавляем формсет для ввода версии продукта
        """
        context_data = super().get_context_data(**kwargs)
        SubjectFormset = inlineformset_factory(
            Product, Version, form=VersionForm, extra=1
        )
        if self.request.method == "POST":
            context_data["formset"] = SubjectFormset(
                self.request.POST, instance=self.object
            )
        else:
            context_data["formset"] = SubjectFormset(instance=self.object)

        return context_data

    def form_valid(self, form):
        """
        Обработка сохранения формсетов
        """
        formset = self.get_context_data()["formset"]
        self.object = form.save()
        if formset.is_valid():
            formset.instance = self.object
            formset.save()

        return super().form_valid(form)

    def get_form_class(self):
        """
        Проверка, что пользователь владелец товара,
        Проверка прав модератора на редактирование товара
        """
        user = self.request.user
        if user == self.object.owner:
            return ProductForm
        if (
                user.has_perm("catalog.set_published_status")
                and user.has_perm("catalog.can_edit_description")
                and user.has_perm("catalog.can_edit_category")
        ):
            return ProductModeratorForm
        raise PermissionDenied


class ProductDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """
    Контроллер удаления товара
    """

    model = Product
    success_url = reverse_lazy("catalog:home")

    def test_func(self):
        """
        проверка на суперюзера
        """
        return self.request.user.is_superuser


class CategoryListView(ListView):
    """
    Контроллер для списка категорий
    """
    model = Category

    def get_queryset(self):
        """
        Вызов сервисной функции, для кэширования
        """
        return get_objects_from_cache(Category)
