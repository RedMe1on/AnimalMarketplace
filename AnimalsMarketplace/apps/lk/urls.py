from django.urls import path
from .views import ProfileViews

app_name = 'lk'


urlpatterns = [
    path('profile/', ProfileViews.as_view(), name='profile')
]
