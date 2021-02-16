from django import template
from django.db.models import QuerySet

from ..models import Post

register = template.Library()


@register.inclusion_tag('blog/tags/popular_post_widget.html')
def popular_post_widget(count: int) -> dict:
    popular_post = Post.objects.order_by('views')[:count]
    return {'popular_post_list': popular_post}
