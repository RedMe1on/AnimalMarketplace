from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import View, ListView, DeleteView, DetailView, UpdateView
from .forms import ProductForm
from .models import Owner, Categories, Product


class ListCategories(ListView):
    model = Categories
    queryset = Categories.objects.order_by('-pub_date')


class ProductList(ListView):
    model = Product
    queryset = Product.objects.order_by('-pub_date')


class CategoriesDetail(DetailView):
    model = Categories


class ProductDetail(DetailView):
    model = Product
    template = 'catalogs/product_detail.html'


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
