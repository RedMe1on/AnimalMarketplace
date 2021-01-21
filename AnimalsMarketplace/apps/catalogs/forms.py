from django import forms
from .models import Product, RatingProduct


class ProductAdminForm(forms.ModelForm):
    """Форма вывода в ряд с виджетом единственного выбора в админке"""
    sex = forms.ChoiceField(widget=forms.RadioSelect(attrs={'class': 'inline'}), choices=Product.SexChoices.choices,
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


class FilterForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('sex', 'breed',)
        widgets = {
            'sex': forms.Select(attrs={'class': 'selectpicker'}),
            'breed': forms.SelectMultiple(attrs={'class': 'selectpicker'},
                                          choices=[(product.breed, product.breed) for product in
                                                   Product.objects.order_by('breed').distinct('breed')]),

        }
