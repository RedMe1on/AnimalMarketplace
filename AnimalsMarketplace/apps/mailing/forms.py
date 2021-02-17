from django import forms
from .models import Mailing


class MailingForm(forms.ModelForm):
    """Форма подписки по email"""

    class Meta:
        model = Mailing
        fields = ('email',)
        widgets = {
            "email": forms.EmailInput(attrs={"placeholder": "example@example.ru", })
        }
        labels = {
            "email": 'E-mail'
        }
