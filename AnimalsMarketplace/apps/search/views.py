from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView
from django.contrib.postgres.search import SearchRank, SearchQuery, SearchVector

from catalogs.models import Product


class SearchViews(ListView):
    model = Product
    template_name = 'search/search.html'

    def get_queryset(self):
        search_vector = SearchVector('name', weight='A') + SearchVector('text', weight='B')
        search_query = SearchQuery(self.request.GET.get('q'))
        search_rank = SearchRank(search_vector, search_query, weights=[0.2, 0.4, 0.6, 0.8])
        if search_query:
            queryset = Product.objects.annotate(rank=search_rank).filter(rank__gte=0.3).order_by('-rank')
        else:
            queryset = None
        return queryset
