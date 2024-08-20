from django.db import models

NULLABLE = {"blank": True, "null": True}


class Product(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name="Наименование",
        help_text="Введите наименование товара",
    )
    description = models.CharField(
        max_length=100, verbose_name="Описание", help_text="Введите описание товара"
    )
    photo = models.ImageField(
        upload_to="product/photo",
        verbose_name="Изображение",
        help_text="Загрузите фото товара",
        **NULLABLE,
    )
    category = models.CharField(
        max_length=50, verbose_name="Категория", help_text="Введите категорию товара"
    )
    price = models.FloatField(
        verbose_name="Цена за покупку", help_text="Введите стоимость товара"
    )
    created_at = models.DateField(
        verbose_name="Дата создания", help_text="Укажите дату записи в БД"
    )
    updated_at = models.DateField(
        verbose_name="Дата последнего изменения",
        help_text="Укажите дату последнего изменения",
    )

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"
        ordering = ["name", "category", "date_create", "date_change"]

    def __str__(self):
        return f"{self.name} {self.category}"


class Category(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name="Название категории",
        help_text="Введите название категории товара",
    )
    description = models.TextField(
        verbose_name="Описание категории",
        help_text="Введите описание категории товара",
        **NULLABLE,
    )

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name
