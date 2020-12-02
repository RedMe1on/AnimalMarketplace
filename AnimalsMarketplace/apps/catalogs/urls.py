from django.urls import path
from .views import CategoriesList, CategoriesDetail, ProductDetail, ProductList, \
    MainPage, AddRatingViews, SearchView

app_name = 'catalogs'
urlpatterns = [
    path('', MainPage.as_view(), name='main'),
    path('categories/', CategoriesList.as_view(), name='categories_list'),
    path('rating-form/', AddRatingViews.as_view(), name='add_rating'),
    path('product/', ProductList.as_view(), name='product_list'),
    path('product/<int:pk>/', ProductDetail.as_view(), name='product_detail'),
    path('search/', SearchView.as_view(), name='search'),
    path('<str:slug>/', CategoriesDetail.as_view(), name='categories_detail'),

]
