from django.urls import path

from search.views import SearchViews, SearchSuggestViews

app_name = 'search'
urlpatterns = [
    path('', SearchViews.as_view(), name='search_url'),
    path('autocomplete/', SearchSuggestViews.as_view(), name='autocomplete'),
]
