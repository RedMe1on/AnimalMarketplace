from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.views.generic import View

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
