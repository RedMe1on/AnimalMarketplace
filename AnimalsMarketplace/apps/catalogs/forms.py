from django import forms
from .models import Product


class ProductForm(forms.Form):
    title = forms.CharField(max_length=50)
    slug = forms.SlugField(max_length=50)
    h1 = forms.CharField(max_length=50)
    description = forms.CharField(max_length=300)
    text = forms.CharField(max_length=10000)

    def save(self):
        new_product = Product.objects.create(title=self.cleaned_data['title'],
                                             slug=self.cleaned_data['slug'],
                                             h1=self.cleaned_data['h1'],
                                             description=self.cleaned_data['description'],
                                             text=self.cleaned_data['text'])
        return new_product
