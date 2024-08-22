from django.core.management import BaseCommand
import json

from config.settings import JSON_FILE_PATH
from catalog.models import Category, Product


class Command(BaseCommand):
    @staticmethod
    def json_read_categories():
        # Здесь мы получаем данные из фикстуры с категориями
        with open(JSON_FILE_PATH) as f:
            categories = json.load(f)
        return [
            category
            for category in categories
            if category["model"] == "catalog.category"
        ]

    @staticmethod
    def json_read_products():
        # Здесь мы получаем данные из фикстуры с продуктами
        with open(JSON_FILE_PATH) as f:
            products = json.load(f)
        return [
            product for product in products if product["model"] == "catalog.product"
        ]

    def handle(self, *args, **options):
        # Удалите все продукты
        Product.objects.all().delete()
        # Удалите все категории
        Category.objects.all().delete()
        # Создайте списки для хранения объектов
        product_for_create = []
        category_for_create = []

        # Обходим все значения категорий из фиктсуры для получения информации об одном объекте
        for category in Command.json_read_categories():
            category_for_create.append(
                Category(
                    id=category["pk"],
                    name=category["fields"]["name"],
                    description=category["fields"]["description"],
                )
            )

        # Создаем объекты в базе с помощью метода bulk_create()
        Category.objects.bulk_create(category_for_create)

        # Обходим все значения продуктов из фиктсуры для получения информации об одном объекте
        for product in Command.json_read_products():
            # получаем категорию из базы данных для корректной связки объектов
            if product["fields"]["category"]:
                category = Category.objects.get(pk=product["fields"]["category"])
            else:
                category = None

            product_for_create.append(
                Product(
                    id=product["pk"],
                    name=product["fields"]["name"],
                    description=product["fields"]["description"],
                    photo=product["fields"]["photo"],
                    category=category,
                    price=product["fields"]["price"],
                    created_at=product["fields"]["created_at"],
                    updated_at=product["fields"]["updated_at"],
                )
            )

        #     # Создаем объекты в базе с помощью метода bulk_create()
        Product.objects.bulk_create(product_for_create)
