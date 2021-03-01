from django.db.models import QuerySet
from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormView
from django.views.generic.list import MultipleObjectMixin
from .forms import FilterForm
from .models import Categories, Product
from .utils import ProductFilterMixin


class ProductList(ProductFilterMixin, FormView, ListView):
    model = Product
    form_class = FilterForm
    paginate_by = 10
    ordering = ['-pub_date']

    def get_queryset(self):
        queryset = self.get_filter_product(super().get_queryset())
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print(context)
        return context


class MainPage(ProductList):
    template_name = 'catalogs/main.html'


class CategoriesList(ListView):
    model = Categories
    queryset = Categories.objects.order_by('-pub_date')


class CategoriesDetail(ProductFilterMixin, DetailView, FormView, MultipleObjectMixin):
    model = Categories
    form_class = FilterForm
    paginate_by = 10
    ordering = ['-pub_date']

    def get_context_data(self, **kwargs):
        object_list = self.get_filter_product(self.get_product_list_for_category())
        context = super().get_context_data(object_list=object_list.order_by('name'), **kwargs)
        context['product_list'] = object_list.order_by('name')
        return context

    def get_product_list_for_category(self) -> QuerySet:
        """Список товаров, которые относятся к дочерним и текущей категории"""
        parents_categories = self.object.get_descendants(include_self=True)
        list_product = Product.objects.filter(category__in=parents_categories)
        return list_product


class ProductDetail(DetailView):
    model = Product
    template_name = 'catalogs/product_detail.html'


class SearchView(ListView):
    paginate_by = 1

    def get_queryset(self):
        return Product.objects.filter(title__icontains=self.request.GET.get('title'))
