from django import forms
from .models import Product
from django.core.exceptions import ValidationError, NON_FIELD_ERRORS
from pytils.translit import slugify


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['title', 'slug', 'h1', 'text']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'slug': forms.TextInput(attrs={'class': 'form-control'}),
            'h1': forms.TextInput(attrs={'class': 'form-control'}),
            'text': forms.TextInput(attrs={'class': 'form-control'})
        }
        error_messages = {
            'slug': {
                'invalid': "Не должен содержать пробелы или буквы разных алфавитов",
            }
        }

    def clean_slug(self):
        new_slug = slugify(self.cleaned_data.get('slug'))
        if new_slug is None:
            new_slug = slugify(self.cleaned_data.get('h1'))
        else:
            new_slug = self.cleaned_data.update({'slug': new_slug})

        if new_slug == 'categories/create/':
            raise ValidationError('Slug may not be create')
        if Product.objects.filter(slug__iexact=new_slug).count():
            raise ValidationError(f'Slug must be unique. We have {new_slug} slug already')
        return new_slug


