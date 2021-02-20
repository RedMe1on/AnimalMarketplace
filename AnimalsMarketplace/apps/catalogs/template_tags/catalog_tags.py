from django import template
from django.db.models import QuerySet

from ..models import Categories, Product

register = template.Library()


@register.simple_tag()
def get_categories():
    return Categories.objects.all()


@register.simple_tag()
def get_last_product_with_img(count: int) -> QuerySet:
    """Получить последние 15-ть товаров с изображением"""
    return Product.objects.order_by('-pub_date').exclude(image__contains='/no_image.png')[:count]


@register.simple_tag(takes_context=True)
def url_replace_for_pagination(context, **kwargs) -> str:
    """Тег для получения всех параметров из запроса и замене номера страниц. Используется в пагинации + фильтрация.
    Пример return: page=2&sex=sex1&sex=sex2&breed=breed"""
    query = context['request'].GET.copy()
    query['page'] = kwargs['page']
    return query.urlencode()


@register.inclusion_tag('catalogs/tags/last_ads.html')
def get_last_product(count: int):
    product = Product.objects.order_by('pub_date')[:count]
    return {'get_last_product': product}


@register.inclusion_tag('catalogs/tags/breadcrumb.html')
def catalog_breadcrumb(objects: QuerySet):
    return {
        'objects': objects
    }


@register.simple_tag(takes_context=True)
def get_sex_select(context: dict) -> list:
    """Получить пол из каталога страницы для динамического фильтра"""
    query = context['object_list']
    sex_select = set()
    for product in query:
        sex_select.add(product.sex)
    return list(sex_select)
