from ckeditor.widgets import CKEditorWidget
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms
from django.core.exceptions import ValidationError
from django.forms import inlineformset_factory
from pytils.translit import slugify
from .models import Profile
from catalogs.models import Product, Categories, BreedType, ProductImage


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
                                                 'data-size': '5', 'data-live-search': 'true', 'container': 'body',
                                                 'onChange': 'change_field_breed_type_with_category_id();'},
                                      ), )
    breed_type = forms.ModelChoiceField(queryset=BreedType.objects.all(), empty_label=None, required=False,
                                        label='Вид породы',
                                        widget=forms.Select(
                                            attrs={'class': 'selectpicker select-input', 'title': 'Вид породы',
                                                   'data-style': 'select-input', }, ),
                                        )

    class Meta:
        model = Product
        fields = (
            'name', 'category', 'text', 'sex', 'breed', 'breed_type', 'age_type', 'age', 'price', 'birthday', 'image')
        widgets = {
            'breed': forms.Select(
                attrs={'class': 'selectpicker select-input', 'title': 'Порода', 'data-style': 'select-input'},
                choices=Product.BreedChoices.choices),
            'birthday': forms.DateInput(attrs={'autocomplete': 'off', 'placeholder': 'дд.мм.гггг'}, ),
            'text': CKEditorUploadingWidget(config_name='form-editor'),
        }


class AdditionalImagesProductForm(forms.ModelForm):
    class Meta:
        model = ProductImage
        fields = ('additional_image',)
        widgets = {
            'additional_image': forms.FileInput(attrs={'multiple': 'multiple'})
        }


ProductFormSet = inlineformset_factory(Product, ProductImage, form=AdditionalImagesProductForm, extra=5,
                                       can_delete=False,
                                       can_order=False)
