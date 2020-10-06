from django.urls import path, reverse
from .views import ProfileViews, ProfileEditViews, ProductEditView, ProductCreateView, ProductListView, \
    ProductDeleteView
from django.views.generic import RedirectView

app_name = 'lk'

urlpatterns = [
    path('', RedirectView.as_view(url='profile/'), name='redirect_from_profile'),
    path('profile/', ProfileViews.as_view(), name='profile'),
    path('profile/edit', ProfileEditViews.as_view(), name='edit_profile'),
    path('product/', ProductListView.as_view(), name='product_list'),
    path('product/create/', ProductCreateView.as_view(), name='product_create'),
    path('product/<int:pk>/delete/', ProductDeleteView.as_view(), name='product_delete'),
    path('product/<int:pk>/update/', ProductEditView.as_view(), name='product_update'),

]
