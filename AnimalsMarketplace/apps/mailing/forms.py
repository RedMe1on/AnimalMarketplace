from django import forms
from .models import Mailing


class MailingForm(forms.ModelForm):
    """Форма подписки по email"""

    class Meta:
        model = Mailing
        fields = ('email',)
        widgets = {
            "email": forms.TextInput(attrs={"placeholder": "Enter your email here...", })
        }
        labels = {
            "email": ''
        }
