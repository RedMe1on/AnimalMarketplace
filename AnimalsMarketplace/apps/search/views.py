from django.shortcuts import render
from elasticsearch_dsl import Q
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
            q = Q("multi_match", query=query, fields=['name', 'text'])
            queryset = ProductDocument.search().query(q)
        else:
            queryset = None
        return queryset
