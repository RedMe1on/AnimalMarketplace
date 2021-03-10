from ckeditor.widgets import CKEditorWidget
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms
from django.core.exceptions import ValidationError
from pytils.translit import slugify
from .models import Profile
from catalogs.models import Product, Categories


class ProfileEditForm(forms.ModelForm):
    """Форма редактирования профиля"""

    class Meta:
        model = Profile
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Имя'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Фамилия'}),
            'email': forms.EmailInput(attrs={'placeholder': 'example@example.ru'}),
            'phone_number': forms.TextInput(attrs={'placeholder': '+7 (XXX) XXX-XX-XX'}),
            'phone_number_ads': forms.TextInput(attrs={'placeholder': '+7 (XXX) XXX-XX-XX'}),
        }
        labels = {
            'name': 'Имя',
            'last_name': 'Фамилия',
            'email': 'Электронная почта',
            'phone_number': 'Телефон',
            'phone_number_ads': 'Телефон для объявлений'
        }
        exclude = ('user',)
        error_messages = {
            'phone_number': {
                'invalid': "Введите телефон в формате +7 (XXX) XXX-XX-XX",
            },
            'phone_number_ads': {
                'invalid': "Введите телефон в формате +7 (XXX) XXX-XX-XX",
            },
            'email': {
                'invalid': 'Введите правильный адрес электронной почты в формате xxxxx@xxxxx.xx'
            }
        }


class ProductForm(forms.ModelForm):
    """Форма редактирования объявления"""
    sex = forms.ChoiceField(widget=forms.Select(
        attrs={'class': 'selectpicker select-input', 'title': 'Пол', 'data-style': 'select-input'}, ),
        choices=Product.SexChoices.choices, label='Пол питомца')
    category = forms.ModelChoiceField(queryset=Categories.objects.all(), empty_label=None,
                                      label='Родительская категория',
                                      widget=forms.Select(
                                          attrs={'class': 'selectpicker select-input', 'title': 'Категория',
                                                 'data-style': 'select-input',
                                                 'data-size': '5', 'data-live-search': 'true', 'container': 'body'},
                                      ), )

    class Meta:
        model = Product
        fields = ('name', 'category', 'text', 'sex', 'breed', 'breed_type', 'age_type', 'age', 'price', 'birthday', 'image')
        widgets = {
            'breed': forms.Select(
                attrs={'class': 'selectpicker select-input', 'title': 'Порода', 'data-style': 'select-input'},
                choices=Product.BreedChoices.choices),
            'breed_type': forms.Select(
                attrs={'class': 'selectpicker select-input', 'title': 'Порода', 'data-style': 'select-input'},
                choices=Product.BreedChoices.choices),
            'birthday': forms.DateInput(attrs={'autocomplete': 'off', 'placeholder': 'дд.мм.гггг'}, ),
            'text': CKEditorUploadingWidget(config_name='form-editor'),

        }
