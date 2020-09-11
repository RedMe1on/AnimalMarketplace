from django.urls import path

from .views import MailingView, ThanksView

app_name = 'mailings'
urlpatterns = [
    path('', MailingView.as_view(), name='mailing'),
    path('thanks/', ThanksView.as_view(), name='thanks_mailing'),
]
