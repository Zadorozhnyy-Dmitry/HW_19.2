from datetime import datetime

from django.db import models

NULLABLE = {"blank": True, "null": True}


class Blog(models.Model):
    title = models.CharField(max_length=150, verbose_name="Заголовок")
    slug = models.CharField(max_length=150, verbose_name="slug", **NULLABLE)
    body = models.TextField(verbose_name="Содержимое")
    preview = models.ImageField(
        upload_to="blog/photo",
        verbose_name="Изображение",
        **NULLABLE,
    )
    created_at = models.DateField(
        default=datetime.now,
        verbose_name="Дата создания",
    )
    is_published = models.BooleanField(default=True, verbose_name="Опубликовано")
    views_count = models.IntegerField(default=0, verbose_name="Просмотры")

    def __str__(self):
        return f"{self.title} {self.created_at}"

    class Meta:
        verbose_name = "блог"
        verbose_name_plural = "блог"
