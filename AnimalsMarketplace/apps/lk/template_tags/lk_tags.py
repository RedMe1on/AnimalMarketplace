from django import template

register = template.Library()


@register.inclusion_tag('lk/template_tags/file_upload.html')
def get_max_number_img(max_number: int) -> dict:
    """Возвращает число максимального количества загружаемых изображений для превью"""
    return {'max_number': max_number}


@register.simple_tag()
def get_sub_max_number_and_current_number_img(max_number: int, current_number: int):
    """Получить доступное количество загружаемых изображений"""
    return max_number - current_number
