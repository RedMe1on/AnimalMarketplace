from django.views.generic import DetailView
from django.views.generic.list import MultipleObjectMixin, ListView

from .models import Post, Categories, BlogTags


class PostDetailView(DetailView):
    """Детальная публикация"""
    model = Post
    template_name = 'blog/blog_detail.html'


class CategoriesDetailView(DetailView, MultipleObjectMixin):
    """Детальная категория"""
    model = Categories
    template_name = 'blog/blog_categories.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        object_list = Post.objects.filter(category_id=self.object).order_by('-pub_date')
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['post_list'] = context['object_list']
        return context


class CategoriesListView(ListView):
    """Список категорий - для главной блога: /blog/"""
    model = Categories
    queryset = Categories.objects.order_by('-priority')[:3]
    template_name = 'blog/blog_main.html'

    def get_context_data(self, **kwargs):
        post = Post.objects.all().order_by('-pub_date')
        context = super().get_context_data(**kwargs)
        context['post_list'] = post
        return context


class BlogTagsView(DetailView, MultipleObjectMixin):
    """Теги для постов блога"""
    model = BlogTags
    template_name = 'blog/tag_detail.html'
    paginate_by = 2

    def get_context_data(self, **kwargs):
        post = self.object.post_set.all().order_by('-pub_date')
        context = super().get_context_data(object_list=post, **kwargs)
        context['post_list'] = context['object_list']
        return context
