from catalog.models import Product
from config.settings import CACHE_ENABLE
from django.core.cache import cache


def get_products_from_cache():
    """
    Сервисная функция выдает список товаров, если он есть в кэше
    Если кэш пуст, получает данные из БД
    """
    if not CACHE_ENABLE:
        return Product.objects.all()
    key = "products_list"
    products = cache.get(key)
    if products is not None:
        return products
    products = Product.objects.all()
    cache.set(key, products)
    return products
