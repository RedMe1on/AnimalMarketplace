from django.urls import path

from search.views import SearchViews, SearchSuggestViews

app_name = 'search'
urlpatterns = [
    path('', SearchViews.as_view(), name='search'),
    path('autocomplete/', SearchSuggestViews.as_view(), name='autocomplete'),
]
