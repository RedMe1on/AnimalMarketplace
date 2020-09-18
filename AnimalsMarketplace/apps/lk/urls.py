from django.urls import path, reverse
from .views import ProfileViews, ProfileEditViews
from django.views.generic import RedirectView

app_name = 'lk'

urlpatterns = [
    path('', RedirectView.as_view(url='profile/'), name='redirect_from_profile'),
    path('profile/', ProfileViews.as_view(), name='profile'),
    path('profile/edit', ProfileEditViews.as_view(), name='edit_profile'),

]
