from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, redirect, reverse
from django.views.generic import View
from .forms import ProductForm
from .models import Owner, Categories, Product
from .utils import ObjectDetailMixin, ObjectListMixin, ObjectUpdateMixin, ObjectDeleteMixin


class ListCategories(ObjectListMixin, View):
    model = Categories
    template = 'catalogs/categories_list.html'


class ProductList(ObjectListMixin, View):
    model = Product
    template = 'catalogs/product_list.html'


class CategoriesDetail(ObjectDetailMixin, View):
    model = Categories
    template = 'catalogs/categories_detail.html'


class ProductDetail(ObjectDetailMixin, View):
    model = Product
    template = 'catalogs/product_detail.html'


class ProductUpdate(ObjectUpdateMixin, View):
    model = Product
    form_model = ProductForm
    template = 'catalogs/product_update_form.html'


class ProductDelete(ObjectDeleteMixin, View):
    model = Product
    template = 'catalogs/product_delete.html'
    redirect_url = 'catalogs:product_list'


class ProductCreate(View):

    def get(self, request):
        form = ProductForm()
        return render(request, 'catalogs/product_create.html', context={'form': form})

    def post(self, request):
        bound_form = ProductForm(request.POST)
        if bound_form.is_valid():
            new_product = bound_form.save(commit=False)
            new_product.owner = Owner.objects.get(id=1)
            new_product = bound_form.save()
            return redirect(new_product)
        return render(request, 'catalogs/product_create.html', context={'form': bound_form})
