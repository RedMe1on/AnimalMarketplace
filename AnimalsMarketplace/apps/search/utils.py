from django.http.response import JsonResponse
from django.views import View
from django.views.generic import FormView, ListView
from elasticsearch_dsl import Q, Document

from search.forms import SearchForm


class ListSearchMixin(FormView, ListView):
    """Миксин для поиска"""
    model = None
    search_document = None
    additional_dict_model_documents = {}  # key=name_search, value={model: Model, document:Document, fields:[str, str, ..., str]}
    template_name = 'search/search.html'
    paginate_by = 10
    form_class = SearchForm

    def get_queryset(self):
        input_text = self.request.GET.get('q')
        if input_text:
            q = Q("multi_match", query=input_text, fields=['name', 'text'])
            queryset = self.search_document.search().query(q)

            search_id_list = [obj.id for obj in queryset[:100]]
            queryset_dict = self.model.objects.in_bulk(id_list=search_id_list)
            queryset = [queryset_dict[id] for id in search_id_list]
        else:
            queryset = []
        return queryset

    def get_additional_queryset(self, search_config: dict) -> list:
        """Получение дополнительных queryset для поиска"""
        input_text = self.request.GET.get('q')
        if input_text:
            q = Q("multi_match", query=input_text, fields=search_config.get('fields'))
            queryset = search_config.get('document').search().query(q)

            search_id_list = [obj.id for obj in queryset[:100]]
            queryset_dict = search_config.get('model').objects.in_bulk(id_list=search_id_list)
            additional_queryset = [queryset_dict[id] for id in search_id_list]
        else:
            additional_queryset = []
        return additional_queryset

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        if self.additional_dict_model_documents:
            for name_search in self.additional_dict_model_documents:
                ctx[f'{name_search}'] = self.get_additional_queryset(self.additional_dict_model_documents[name_search])
        if self.request.GET:
            ctx['form'] = SearchForm(self.request.GET)
        return ctx


class SearchSuggestMixin(View):
    dict_model_documents = {}  # key=name_search, value={document:Document, field: str}

    def get(self, request, *args, **kwargs):
        input_text = request.GET.get('q')
        if input_text and self.dict_model_documents:
            model_results_dict = {}
            for name_search in self.dict_model_documents:
                name_search_value = self.dict_model_documents[name_search]
                field = name_search_value.get('field')
                dict_for_query = {field: input_text}

                query = Q("match", **dict_for_query)
                queryset = name_search_value.get('document').search().query(query).suggest(
                    'search_suggestion', input_text, completion={'field': f'{field}.suggest'})

                results = [{'id': result.id, f'{field}': result.name} for result in queryset]
                model_results_dict[f'{name_search}'] = results
            model_results = [model_results_dict]
        else:
            model_results = []
        return JsonResponse({'results': model_results}, json_dumps_params={'ensure_ascii': False})
