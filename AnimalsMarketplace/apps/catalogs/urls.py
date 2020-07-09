from django.urls import path
from .views import ListCategories, CategoriesDetail


app_name = 'catalogs'
urlpatterns = [
    path('', ListCategories.as_view(), name='ListPost'),
    path('<str:slug>/', CategoriesDetail.as_view(), name='CategoriesDetail')
]
