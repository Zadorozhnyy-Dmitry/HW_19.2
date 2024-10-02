from django.shortcuts import render
from django.views.generic import (
    CreateView,
    ListView,
    DetailView,
    UpdateView,
    DeleteView,
)
from django.urls import reverse_lazy, reverse

from blog.models import Blog

from pytils.translit import slugify
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin


class BlogCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    """
    Контроллер создания сообщения
    """

    model = Blog
    fields = (
        "title",
        "body",
        "preview",
    )
    permission_required = "blog.add_blog"
    success_url = reverse_lazy("blog:list")

    def form_valid(self, form):
        """
        Формирования slug для названия сообщения
        """
        if form.is_valid():
            new_blog = form.save()
            new_blog.slug = slugify(new_blog.title)
            new_blog.save()
        return super().form_valid(form)


class BlogUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    """
    Контроллер редактирования сообщения
    """

    model = Blog
    fields = (
        "title",
        "body",
        "preview",
    )
    permission_required = "blog.change_blog"

    def form_valid(self, form):
        """
        Формирования slug для названия сообщения
        """
        if form.is_valid():
            new_blog = form.save()
            new_blog.slug = slugify(new_blog.title)
            new_blog.save()
        return super().form_valid(form)

    def get_success_url(self):
        """
        Перенаправление на нужное сообщение после редактирования
        """
        return reverse("blog:view", args=[self.kwargs.get("pk")])


class BlogListView(ListView):
    """
    Контроллер страницы просмотра сообщений блога
    """

    model = Blog

    def get_queryset(self, *args, **kwargs):
        """
        Отображение тоалько опубликованных сообщений
        """
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(is_published=True)
        return queryset


class BlogDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    """
    Контроллер детального просмотра сообщений
    """

    model = Blog
    permission_required = "blog.view_blog"

    def get_object(self, queryset=None):
        """
        Счетчик просмотров
        """
        self.object = super().get_object(queryset)
        self.object.views_count += 1
        self.object.save(update_fields=["views_count"])
        return self.object


class BlogDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    """
    Контроллер удаления сообщения
    """

    model = Blog
    permission_required = "blog.delete_blog"
    success_url = reverse_lazy("blog:list")
