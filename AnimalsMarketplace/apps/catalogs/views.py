from django.db.models import QuerySet
from django.http import HttpResponse
from django.views.generic import View, ListView, DetailView
from django.views.generic.list import MultipleObjectMixin
from .forms import RatingForm
from .models import Categories, Product, RatingProduct
from .utils import ProductFilterMixin, RatingProductMixin


class ProductList(ProductFilterMixin, ListView):
    model = Product
    paginate_by = 10
    ordering = ['-pub_date']

    def get_queryset(self):
        queryset = self.get_filter_product(super().get_queryset())
        return queryset


class MainPage(ProductList):
    template_name = 'catalogs/main.html'


class CategoriesList(ProductFilterMixin, ListView):
    model = Categories
    queryset = Categories.objects.order_by('-pub_date')


class CategoriesDetail(ProductFilterMixin, DetailView, MultipleObjectMixin):
    model = Categories
    paginate_by = 2

    def get_context_data(self, **kwargs):
        object_list = self.get_filter_product(self.get_product_list_for_category())
        context = super().get_context_data(object_list=object_list.order_by('name'), **kwargs)
        context['product_list'] = context['object_list']
        context['rating-form'] = RatingForm()
        return context

    def get_product_list_for_category(self) -> QuerySet:
        """Список товаров, которые относятся к дочерним и текущей категории"""
        parents_categories = self.object.get_descendants(include_self=True)
        list_product = Product.objects.filter(category__in=parents_categories)
        return list_product


class ProductDetail(RatingProductMixin, ProductFilterMixin, DetailView):
    model = Product
    rating_model = RatingProduct
    template_name = 'catalogs/product_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rating_form'] = RatingForm()
        context['avg_rating'] = self.get_avg_rating(self.kwargs.get('slug'))
        context['user_rating'] = self.get_user_rating(self.request, self.kwargs.get('slug'))
        return context


class AddRatingViews(RatingProductMixin, View):

    def post(self, request):
        form = RatingForm(request.POST)
        if form.is_valid():
            RatingProduct.objects.update_or_create(
                ip=self.get_client_ip(request),
                product_id=int(request.POST.get('product')),
                defaults={'rating': int(request.POST.get('rating'))}
            )
            return HttpResponse(status=201)
        else:
            return HttpResponse(status=400)


class SearchView(ListView):
    paginate_by = 1

    def get_queryset(self):
        return Product.objects.filter(title__icontains=self.request.GET.get('title'))
