from django.urls import path
from .views import ListCategories, CategoriesDetail, ProductCreate, ProductDetail
from .forms import ProductForm


app_name = 'catalogs'
urlpatterns = [
    path('', ListCategories.as_view(), name='ListCategories'),
    path('categories/create/', ProductCreate.as_view(), name='ProductCreate'),
    path('<str:slug>/', ProductDetail.as_view(), name='ProductDetail'),
    path('<str:slug>/', CategoriesDetail.as_view(), name='CategoriesDetail')
]
