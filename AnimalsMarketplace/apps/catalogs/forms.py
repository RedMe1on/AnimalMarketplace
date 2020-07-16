from django import forms
from .models import Product
from django.core.exceptions import ValidationError
from pytils.translit import slugify


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['title', 'slug', 'h1', 'text']
        # widgets = {
        #     'title': forms.TextInput(attrs={'class': 'form-control'})
        # }

    def clean_slug(self):
        new_slug = slugify(self.cleaned_data['slug'])

        if new_slug == 'categories/create/':
            raise ValidationError('Slug may not be create')
        if Product.objects.filter(slug__iexact=new_slug).count():
            raise ValidationError(f'Slug must be unique. We have {new_slug} slug already')
        return new_slug

    def save(self):
        new_product = Product.objects.create(title=self.cleaned_data['title'],
                                             slug=self.cleaned_data['slug'],
                                             h1=self.cleaned_data['h1'],
                                             text=self.cleaned_data['text'],
                                             owner=self.cleaned_data['owner'])
        return new_product
