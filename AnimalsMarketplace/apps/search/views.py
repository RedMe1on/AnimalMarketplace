from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView

from catalogs.models import Product

from search.documents import ProductDocument


class SearchViews(ListView):
    model = Product
    template_name = 'search/search.html'

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            queryset = ProductDocument.search().filter('match', name=query)
        else:
            queryset = None
        return queryset
