from django.db.models import QuerySet
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import View, ListView, DeleteView, DetailView, UpdateView
from mptt.querysets import TreeQuerySet
from .forms import ProductForm, RatingForm
from .models import Owner, Categories, Product, RatingProduct
from .utils import ProductFilterMixin, RatingProductMixin


class MainPage(ProductFilterMixin, ListView):
    model = Product
    template_name = 'catalogs/main.html'


class CategoriesList(ProductFilterMixin, ListView):
    model = Categories
    queryset = Categories.objects.order_by('-pub_date')


class ProductList(ProductFilterMixin, ListView):
    model = Product
    queryset = Product.objects.order_by('-pub_date')


class CategoriesDetail(ProductFilterMixin, DetailView):
    model = Categories

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product_list'] = self.get_product_list_for_context()
        context['rating-form'] = RatingForm()
        return context

    def get_child_and_self_categories(self, slug: str) -> TreeQuerySet:
        """Метод для получения дочерних категорий и самой категории"""
        category = self.model.objects.get(slug=slug)
        return category.get_descendants(include_self=True)

    def get_product_list_for_context(self) -> QuerySet:
        """Список товаров, которые относятся к дочерним и текущей категории"""
        parents_categories = self.get_child_and_self_categories(self.kwargs.get('slug'))
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


class ProductUpdate(UpdateView):
    model = Product
    template_name_suffix = '_update_form'
    form_class = ProductForm


class ProductDelete(DeleteView):
    model = Product
    success_url = reverse_lazy('catalogs:product_list')
    template_name_suffix = '_delete'


class ProductCreate(View):

    def get(self, request):
        form = ProductForm()
        return render(request, 'catalogs/product_create.html', context={'form': form})

    def post(self, request):
        bound_form = ProductForm(request.POST)
        if bound_form.is_valid():
            new_product = bound_form.save(commit=False)
            new_product.owner_id = 1
            new_product = bound_form.save()
            return redirect(new_product)
        return render(request, 'catalogs/product_create.html', context={'form': bound_form})


class FilterProductViews(CategoriesDetail, ProductFilterMixin):
    """Фильтр карточек товаров на категориях"""

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        filter_product_list = context.get('product_list')
        filter_product_list = filter_product_list.filter(sex__in=self.request.GET.getlist('sex'))
        context['product_list'] = filter_product_list
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
