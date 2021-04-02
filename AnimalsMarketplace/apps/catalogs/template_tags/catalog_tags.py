from django import template
from django.db.models import QuerySet
from ..models import Categories, Product, ProductImage
from blog.models import Categories as Categories_blog

register = template.Library()


@register.simple_tag()
def get_categories():
    return Categories.objects.all()


@register.simple_tag()
def get_categories_blog():
    return Categories_blog.objects.all()


@register.simple_tag()
def get_phone_number(phone_number) -> str:
    phone_number_str = str(phone_number)
    return f'+7 ({phone_number_str[2:5]}) {phone_number_str[5:8]}-{phone_number_str[8:10]}-{phone_number_str[10:12]}'


@register.simple_tag()
def get_last_product_with_img(count: int) -> QuerySet:
    """Получить последние n товаров с изображением"""
    return Product.objects.order_by('-pub_date').filter(
        additional_img__image__contains='catalogs/product/img').distinct()[:count]


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
    try:
        sex_select = [product.sex for product in
                      Product.objects.filter(category=context['categories']).order_by('sex').distinct(
                          'sex')]
    except KeyError:
        sex_select = [product.sex for product in Product.objects.all().order_by('sex').distinct(
            'sex')]
    return sex_select


@register.simple_tag(takes_context=True)
def get_breed_type_select(context: dict) -> list:
    """Получить тип породы из каталога страницы для динамического фильтра"""
    try:
        breed_type_select = [product.breed_type for product in
                             Product.objects.filter(category=context['categories']).select_related(
                                 'breed_type').order_by('breed_type').distinct(
                                 'breed_type')]
    except KeyError:
        breed_type_select = [product.breed_type for product in
                             Product.objects.all().select_related('breed_type').order_by('breed_type').distinct(
                                 'breed_type')]
    return breed_type_select


@register.simple_tag(takes_context=True)
def get_breed_select(context: dict) -> list:
    """Получить породы из каталога страницы для динамического фильтра"""
    try:
        breed_select = [product.breed for product in
                        Product.objects.filter(category=context['categories']).order_by('breed').distinct(
                            'breed')]
    except KeyError:
        breed_select = [product.breed for product in
                        Product.objects.all().order_by('breed').distinct(
                            'breed')]
    return breed_select
