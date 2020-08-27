from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms
from .models import Product, RatingProduct
from django.core.exceptions import ValidationError
from pytils.translit import slugify


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'h1': forms.TextInput(attrs={'class': 'form-control'}),
            'slug': forms.TextInput(attrs={'class': 'form-control'}),
            'text': forms.TextInput(attrs={'class': 'form-control'})
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


class ProductAdminForm(forms.ModelForm):
    FEMALE = 'Девочка'
    MALE = 'Мальчик'
    SEX_CHOICES = (
        (FEMALE, 'Девочка'),
        (MALE, 'Мальчик')
    )
    text = forms.CharField(label='Текст', widget=CKEditorUploadingWidget(), required=False)
    sex = forms.ChoiceField(widget=forms.RadioSelect(attrs={'class': 'inline'}), choices=SEX_CHOICES,
                            label='Пол питомца')

    class Meta:
        model = Product
        fields = '__all__'


class RatingForm(forms.ModelForm):
    """Форма добавления рейтинга"""
    rating = forms.ChoiceField(widget=forms.RadioSelect(), choices=RatingProduct.Star.choices)

    class Meta:
        model = RatingProduct
        fields = ('rating',)

