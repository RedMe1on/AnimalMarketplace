from django.urls import path
from .views import CategoriesList, CategoriesDetail, ProductDetail, ProductList, \
    MainPage, BreedTypeListAPIView, ReportView, SuccessReportView

app_name = 'catalogs'
urlpatterns = [
    path('', MainPage.as_view(), name='main'),
    path('categories/', CategoriesList.as_view(), name='categories_list'),
    path('report/<int:pk>/', ReportView.as_view(), name='report'),
    path('report/success/', SuccessReportView.as_view(), name='report_success'),
    path('product/', ProductList.as_view(), name='product_list'),
    path('product/<int:pk>/', ProductDetail.as_view(), name='product_detail'),
    path('<str:slug>/', CategoriesDetail.as_view(), name='categories_detail'),
    path('api/v1/breedtype/', BreedTypeListAPIView.as_view()),
]
