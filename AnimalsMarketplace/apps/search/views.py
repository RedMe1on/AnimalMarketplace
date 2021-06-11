from django.http.response import JsonResponse
from django.views import View
from elasticsearch_dsl import Q
from django.views.generic import ListView, FormView

from catalogs.models import Product
from search.documents import ProductDocument
from search.forms import SearchForm


class SearchViews(FormView, ListView):
    model = Product
    template_name = 'search/search.html'
    paginate_by = 10
    form_class = SearchForm
    search_document = ProductDocument

    def get_queryset(self):
        input_text = self.request.GET.get('q')
        if input_text:
            q = Q("multi_match", query=input_text, fields=['name', 'text'])
            queryset = self.search_document.search().query(q)

            search_id_list = [obj.id for obj in queryset[:30]]
            queryset_dict = Product.objects.in_bulk(id_list=search_id_list)
            queryset = [queryset_dict[id] for id in search_id_list]
        else:
            queryset = []
        return queryset

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        if self.request.GET:
            ctx['form'] = SearchForm(self.request.GET)
        return ctx



class SearchSuggestViews(View):
    search_document = ProductDocument

    def get(self, request, *args, **kwargs):
        input_text = request.GET.get('q')
        if input_text:
            query = Q("match", name=input_text)
            queryset = self.search_document.search().query(query).suggest('search_suggestion', input_text,
                                                                          completion={'field': 'name.suggest'})

            results = [{'id': result.id, 'name': result.name} for result in queryset]
        else:
            results = None
        return JsonResponse({'results': results}, json_dumps_params={'ensure_ascii': False})


# class BlogSearch