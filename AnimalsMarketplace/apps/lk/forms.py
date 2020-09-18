from django import forms

from .models import Profile


class ProfileEditForm(forms.ModelForm):
    """Форма редактирования профиля"""
    class Meta:
        model = Profile
        exclude = ('user',)