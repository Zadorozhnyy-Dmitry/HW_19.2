from catalog.models import Product, Category
from config.settings import CACHE_ENABLE
from django.core.cache import cache


def get_objects_from_cache(MyObject):
    """
    Сервисная функция выдает список товаров, если он есть в кэше
    Если кэш пуст, получает данные из БД
    """
    if not CACHE_ENABLE:
        return MyObject.objects.all()
    key = None
    if MyObject == Product:
        key = "product_list"
    elif MyObject == Category:
        key = "category_list"
    my_objects = cache.get(key)
    if my_objects is not None:
        return my_objects
    my_objects = MyObject.objects.all()
    cache.set(key, my_objects)
    return my_objects
