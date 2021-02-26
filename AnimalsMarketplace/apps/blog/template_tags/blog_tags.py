from django import template
from django.db.models import QuerySet
from django.core.exceptions import ObjectDoesNotExist
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


@register.inclusion_tag('blog/tags/prev_next_posts_widget.html')
def prev_next_posts_widget(post: QuerySet) -> dict:
    """Previously and next posts"""
    try:
        prev_post = post.get_previous_by_pub_date()
    except ObjectDoesNotExist:
        prev_post = Post.objects.last()
    try:
        next_post = post.get_next_by_pub_date()
    except ObjectDoesNotExist:
        next_post = Post.objects.first()
    return {'prev_post': prev_post, 'next_post': next_post}


@register.inclusion_tag('blog/tags/topic_posts_widget.html')
def topic_posts_widget(post: QuerySet) -> dict:
    """topic posts block for blog"""
    topic_posts = Post.objects.filter(category=post.category)
    return {'topic_posts': topic_posts}
