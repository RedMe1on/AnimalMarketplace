from django.urls import path
from .views import CategoriesList, CategoriesDetail, ProductCreate, ProductDetail, ProductUpdate, ProductList, \
    ProductDelete, MainPage, AddRatingViews, SearchView

app_name = 'catalogs'
urlpatterns = [
    path('', MainPage.as_view(), name='main'),
    path('categories/', CategoriesList.as_view(), name='categories_list'),
    path('rating-form/', AddRatingViews.as_view(), name='add_rating'),
    path('product/', ProductList.as_view(), name='product_list'),
    path('search/', SearchView.as_view(), name='search'),
    path('product/create/', ProductCreate.as_view(), name='product_create'),
    path('product/<str:slug>/', ProductDetail.as_view(), name='product_detail'),
    path('product/<str:slug>/update/', ProductUpdate.as_view(), name='product_update'),
    path('product/<str:slug>/delete/', ProductDelete.as_view(), name='product_delete'),
    path('<str:slug>/', CategoriesDetail.as_view(), name='categories_detail'),

]
