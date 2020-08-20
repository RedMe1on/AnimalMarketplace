from django import template
from ..models import Categories, Product

register = template.Library()


@register.simple_tag()
def get_categories():
    return Categories.objects.all()


@register.inclusion_tag('catalogs/tags/last_ads.html')
def get_last_product(count):
    product = Product.objects.order_by('pub_date')[:count]
    return {'get_last_product': product}
