from django import forms


class ProductForm(forms.Form):
    title = forms.CharField(max_length=50)
    slug = forms.SlugField(max_length=50)
    h1 = forms.CharField(max_length=50)
    description = forms.CharField(max_length=300)
    text = forms.CharField(max_length=10000)
