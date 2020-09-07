from django import template

from ..models import Categories, Product

register = template.Library()


@register.simple_tag()
def get_categories():
    return Categories.objects.all()


@register.simple_tag(takes_context=True)
def url_replace_for_pagination(context, **kwargs) -> str:
    """Тег для получения всех параметров из запроса и замене номера страниц. Используется в пагинации + фильтрация.
    Пример return: page=2&sex=sex1&sex=sex2&breed=breed"""
    query = context['request'].GET.copy()
    query['page'] = kwargs['page']
    return query.urlencode()


@register.inclusion_tag('catalogs/tags/last_ads.html')
def get_last_product(count):
    product = Product.objects.order_by('pub_date')[:count]
    return {'get_last_product': product}
