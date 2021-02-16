from django.views.generic import DetailView
from django.views.generic.list import MultipleObjectMixin, ListView

from .models import Post, Categories


class PostDetailView(DetailView):
    """Детальная публикация"""
    model = Post
    template_name = 'blog/blog_detail.html'


class CategoriesDetailView(DetailView, MultipleObjectMixin):
    """Детальная категория"""
    model = Categories
    template_name = 'blog/blog_categories.html'
    paginate_by = 2

    def get_context_data(self, **kwargs):
        post = Post.objects.filter(category_id=self.object).order_by('-pub_date')
        context = super().get_context_data(object_list=post, **kwargs)
        context['post_list'] = context['object_list']
        return context


class CategoriesListView(ListView):
    """Список категорий - для главной блога: /blog/"""
    model = Categories
    queryset = Categories.objects.order_by('-pub_date')
    template_name = 'blog/blog_categories_list.html'

