from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, redirect, reverse
from django.views.generic import View

from .forms import ProductForm
from .models import Owner, Categories, Product
from .utils import ObjectDetailMixin, ObjectListMixin, ObjectUpdateMixin


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
    # def get(self, request, slug):
    #     product = Product.objects.get(slug__iexact=slug)
    #     bound_form = ProductForm(instance=product)
    #     return render(request, 'catalogs/product_update_form.html', context={'form': bound_form, 'product': product})
    #
    # def post(self, request, slug):
    #     product = Product.objects.get(slug__iexact=slug)
    #     bound_form = ProductForm(request.POST, instance=product)
    #     if bound_form.is_valid():
    #         edit_product = bound_form.save()
    #         return redirect(edit_product)
    #     return render(request, 'catalogs/product_update_form.html', context={'form': bound_form, 'product': product})


class ProductDelete(View):
    def get(self, request, slug):
        product = Product.objects.get(slug__iexact=slug)
        return render(request, 'catalogs/product_delete.html', context={'product': product})

    def post(self, request, slug):
        product = Product.objects.get(slug__iexact=slug)
        product.delete()
        return redirect(reverse('catalogs:product_list'))


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
