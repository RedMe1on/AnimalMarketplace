from django import template
from django.db.models import QuerySet

from ..models import Post, Categories, BlogTags

register = template.Library()


@register.inclusion_tag('blog/tags/popular_post_widget.html')
def popular_post_widget(count: int) -> dict:
    """Most popular post"""
    popular_post = Post.objects.order_by('views')[:count]
    return {'popular_post_list': popular_post}


@register.inclusion_tag('blog/tags/categories_menu_widget.html')
def categories_menu_widget() -> dict:
    """All categories"""
    categories_list = Categories.objects.all()
    return {'categories_list': categories_list}


@register.inclusion_tag('blog/tags/tag_cloud_widget.html')
def tag_cloud_widget() -> dict:
    """All tag in cloud"""
    tags_list = BlogTags.objects.all()
    return {'tags_list': tags_list}
