from django.urls import path

from .views import CategoriesListView, CategoriesDetailView, PostDetailView, BlogTagsView

app_name = 'blog'

urlpatterns = [
    path('', CategoriesListView.as_view(), name='categories_list'),
    path('<str:slug>/', CategoriesDetailView.as_view(), name='categories_detail'),
    path('post/<str:slug>/', PostDetailView.as_view(), name='post_detail'),
    path('tag/<str:slug>/', BlogTagsView.as_view(), name='tag_detail')
]
