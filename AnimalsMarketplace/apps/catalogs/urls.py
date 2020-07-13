from django.urls import path
from .views import ListCategories, CategoriesDetail, ProductCreate
from .forms import ProductForm


app_name = 'catalogs'
urlpatterns = [
    path('', ListCategories.as_view(), name='ListPost'),
    path('categories/create/', ProductCreate.as_view(), name='ProductCreate'),
    path('<str:slug>/', CategoriesDetail.as_view(), name='CategoriesDetail')
]
