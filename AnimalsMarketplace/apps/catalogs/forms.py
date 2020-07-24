from django import forms
from .models import Product
from django.core.exceptions import ValidationError
from pytils.translit import slugify


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['title', 'h1', 'slug',  'text']
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
