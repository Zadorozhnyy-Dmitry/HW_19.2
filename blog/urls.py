from django.urls import path, include
from blog.apps import BlogConfig
from blog.views import BlogCreateView, BlogListView, BlogDetailView, BlogUpdateView, BlogDeleteView

app_name = BlogConfig.name

urlpatterns = [
    path("", BlogListView.as_view(), name="list"),
    path('view/<int:pk>', BlogDetailView.as_view(), name='view'),
    path("create/", BlogCreateView.as_view(), name="create"),
    path('edit/<int:pk>', BlogUpdateView.as_view(), name='update'),
    path('delete/<int:pk>', BlogDeleteView.as_view(), name='delete'),
]
