import json

from django.http.response import JsonResponse
from django.views import View
from django.core import serializers
from elasticsearch_dsl import Q
# Create your views here.
from django.views.generic import ListView

from catalogs.models import Product

from search.documents import ProductDocument


class SearchViews(ListView):
    model = Product
    template_name = 'search/search.html'
    paginate_by = 10

    def get_queryset(self):
        input_text = self.request.GET.get('q')
        if input_text:
            q = Q("multi_match", query=input_text, fields=['name', 'text'])
            queryset = ProductDocument.search().query(q)

            search_id_list = [obj.id for obj in queryset[:30]]
            queryset_dict = Product.objects.in_bulk(id_list=search_id_list)
            queryset = [queryset_dict[id] for id in search_id_list]
        else:
            queryset = None
        return queryset


class SearchSuggestViews(View):
    def get(self, request, *args, **kwargs):
        input_text = request.GET.get('q')
        if input_text:
            query = Q("match", name=input_text)
            queryset = ProductDocument.search().query(query).suggest('search_suggestion', input_text,
                                                                     completion={'field': 'name.suggest'})
            results = [{'id': result.id, 'name': result.name} for result in queryset]
        else:
            results = None
        return JsonResponse({'results': results}, json_dumps_params={'ensure_ascii': False})
