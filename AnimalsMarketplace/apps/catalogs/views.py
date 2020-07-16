from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import View

from .forms import ProductForm
from .models import Owner, Categories, Product
from .utils import ObjectDetailMixin, ObjectListMixin


# def index(request):
#     list_last_categories = Categories.objects.order_by('-pub_date')
#     return render(request, 'catalogs/list.html', {'list_last_categories': list_last_categories})


class ListCategories(ObjectListMixin, View):
    model = Categories
    template = 'catalogs/list.html'


class CategoriesDetail(ObjectDetailMixin, View):
    model = Categories
    template = 'catalogs/detail.html'


class ProductDetail(ObjectDetailMixin, View):
    model = Product
    template = 'catalogs/product_detail.html'


class ProductCreate(View):

    def get(self, request):
        form = ProductForm()
        return render(request, 'catalogs/product_create.html', context={'form': form})

    def post(self, request):
        bound_form = ProductForm(request.POST)
        if bound_form.is_valid():
            bound_form.cleaned_data.update({'owner': Owner.objects.get(id=1)})
            new_product = bound_form.save()
            return redirect(new_product)
        return render(request, 'catalogs/product_create.html', context={'form': bound_form})
