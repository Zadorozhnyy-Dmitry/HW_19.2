from django.shortcuts import render
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from django.urls import reverse_lazy

from blog.models import Blog


class BlogCreateView(CreateView):
    model = Blog
    fields = ('title', 'body', 'preview',)
    success_url = reverse_lazy('blog:list')


class BlogUpdateView(UpdateView):
    model = Blog
    fields = ('title', 'body', 'preview',)
    success_url = reverse_lazy('blog:list')


class BlogListView(ListView):
    model = Blog


class BlogDetailView(DetailView):
    model = Blog


class BlogDeleteView(DeleteView):
    model = Blog
    success_url = reverse_lazy('blog:list')
