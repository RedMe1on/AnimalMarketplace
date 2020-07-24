from django.urls import path
from .views import ListCategories, CategoriesDetail, ProductCreate, ProductDetail, ProductUpdate, ProductList, \
    ProductDelete

app_name = 'catalogs'
urlpatterns = [
    path('', ListCategories.as_view(), name='list_categories'),
    path('product/', ProductList.as_view(), name='product_list'),
    path('product/create/', ProductCreate.as_view(), name='product_create'),
    path('product/<str:slug>/', ProductDetail.as_view(), name='product_detail'),
    path('product/<str:slug>/update/', ProductUpdate.as_view(), name='product_update'),
    path('product/<str:slug>/delete/', ProductDelete.as_view(), name='product_delete'),
    path('<str:slug>/', CategoriesDetail.as_view(), name='categories_detail'),


]
