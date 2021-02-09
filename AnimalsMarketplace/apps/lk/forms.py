from ckeditor.widgets import CKEditorWidget
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms
from django.core.exceptions import ValidationError
from pytils.translit import slugify
from .models import Profile
from catalogs.models import Product


class ProfileEditForm(forms.ModelForm):
    """Форма редактирования профиля"""

    class Meta:
        model = Profile
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Имя'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Фамилия'}),
            'email': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Электронная почта'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+79999999999'})
        }
        labels = {
            'name': 'Имя',
            'last_name': 'Фамилия',
            'email': 'Электронная почта',
            'phone_number': 'Телефон',
        }
        exclude = ('user',)
        error_messages = {
            'phone_number': {
                'invalid': "Введите телефон в формате +79999999999",
            }
        }


class ProductForm(forms.ModelForm):
    """Форма редактирования объявления"""
    sex = forms.ChoiceField(widget=forms.RadioSelect(attrs={'class': 'form-check-inline m-2'}),
                            choices=Product.SexChoices.choices,
                            label='Пол питомца')

    class Meta:
        model = Product
        fields = ('name', 'category', 'text', 'h1', 'sex', 'birthday', 'breed', 'image', 'draft')
        widgets = {
            'birthday': forms.SelectDateWidget(attrs={'class': 'my-2 d-inline-block', 'style': 'width: 33%;'},
                                               years=range(1940, 2021)),
            'text': CKEditorUploadingWidget(config_name='form-editor'),
        }
        error_messages = {
            'slug': {
                'invalid': "Не должен содержать пробелы или буквы разных алфавитов",
            }
        }

    def clean_slug(self):
        new_slug = self.cleaned_data.get('slug')
        if new_slug is None or new_slug == '':
            new_slug = slugify(self.cleaned_data.get('h1'))
        else:
            new_slug = slugify(new_slug)
        if new_slug == 'product/create/':
            raise ValidationError('Slug may not be create')
        return new_slug
