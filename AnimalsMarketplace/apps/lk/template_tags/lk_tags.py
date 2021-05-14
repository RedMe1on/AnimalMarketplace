from django import template

from AnimalsMarketplace import settings

register = template.Library()


@register.inclusion_tag('lk/template_tags/file_upload.html')
def get_file_upload_with_max_number_img(max_number=settings.MAX_UPLOAD_PHOTO) -> dict:
    """Возвращает шаблон загрузки изображения с максимальным количеством загружаемых изображений для превью"""
    return {'max_number': max_number}


@register.simple_tag()
def get_sub_max_number_and_current_number_img(current_number: int):
    """Получить доступное количество загружаемых изображений"""
    return settings.MAX_UPLOAD_PHOTO - current_number


@register.simple_tag()
def get_max_number_img():
    """Получить максимальное количество загружаемых изображений"""
    return settings.MAX_UPLOAD_PHOTO
