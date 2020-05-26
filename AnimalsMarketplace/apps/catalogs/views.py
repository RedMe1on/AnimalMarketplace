from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render
from .models import Owner, Categories, Product


def index(request):
    list_last_categories = Categories.objects.order_by('-pub_date')
    return render(request, 'catalogs/list.html', {'list_last_categories': list_last_categories})


def detail(request, categories_id: int):
    try:
        categories = Categories.objects.get(id=categories_id)
    except Exception:
        raise Http404('Нет статьи, вали отседова!')

    return render(request, 'catalogs/detail.html', {'categories': categories})
