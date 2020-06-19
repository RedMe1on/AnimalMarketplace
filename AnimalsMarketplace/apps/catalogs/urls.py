from django.urls import path
from .views import ListCategories, PostDetail


app_name = 'catalogs'
urlpatterns = [
    path('', ListCategories.as_view(), name='ListPost'),
    path('<int:id>/', PostDetail.as_view(), name='PostDetail')
]
