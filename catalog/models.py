from django.db import models

from users.models import User

NULLABLE = {"blank": True, "null": True}


class Category(models.Model):
    """
    Модель описывает категории товаров
    """

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


class Product(models.Model):
    """
    Модель описывает товар
    """

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
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        verbose_name="Категория",
        help_text="Введите категорию товара",
        related_name="products",
        **NULLABLE,
    )
    price = models.FloatField(
        verbose_name="Цена за покупку", help_text="Введите стоимость товара"
    )
    created_at = models.DateField(
        auto_now_add=True,
        verbose_name="Дата создания",
        help_text="Укажите дату записи в БД",
    )
    updated_at = models.DateField(
        auto_now=True,
        verbose_name="Дата последнего изменения",
        help_text="Укажите дату последнего изменения",
    )

    owner = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        verbose_name="Владелец",
        help_text="Введите владельца товара",
        related_name="products",
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"
        ordering = ["name", "category", "created_at", "updated_at"]

    def __str__(self):
        return f"{self.name} {self.category}"


class Version(models.Model):
    """
    Модель описывает версию товара
    """

    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="товар")
    number_of_version = models.FloatField(verbose_name="номер версии")
    title = models.CharField(max_length=150, verbose_name="название версии")
    is_actual = models.BooleanField(
        default=False, verbose_name="признак текущей версии"
    )

    def __str__(self):
        return f"{self.title}.версия {self.number_of_version}"

    class Meta:
        verbose_name = "Версия"
        verbose_name_plural = "Версии"
        ordering = (
            "product",
            "is_actual",
        )
