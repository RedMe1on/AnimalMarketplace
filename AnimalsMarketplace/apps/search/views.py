from django.shortcuts import render
from elasticsearch_dsl import Q, tokenizer, analyzer, SF
# Create your views here.
from django.views.generic import ListView

from catalogs.models import Product

from search.documents import ProductDocument


class SearchViews(ListView):
    model = Product
    template_name = 'search/search.html'

    def get_queryset(self):
        query = self.request.GET.get('q')
        q = Q("multi_match", query=query, fields=['name', 'text'])
        # query = Q(
        #     'function_score',
        #     query=q,
        #     # functions=[
        #     #     SF('field_value_factor', field='name')
        #     # ]
        # )
        if query:

            queryset = ProductDocument.search().query(q)
           # for q in queryset:
            #     print(q)
        else:
            queryset = None
        return queryset
