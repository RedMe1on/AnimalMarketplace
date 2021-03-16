from django import forms
from .models import Product
from django.db.utils import ProgrammingError as AvoidDataMigrationError


class ProductAdminForm(forms.ModelForm):
    """Форма вывода в ряд с виджетом единственного выбора в админке"""
    sex = forms.ChoiceField(widget=forms.RadioSelect(attrs={'class': 'inline'}), choices=Product.SexChoices.choices,
                            label='Пол питомца')

    class Meta:
        model = Product
        fields = '__all__'


class FilterForm(forms.ModelForm):
    image = forms.BooleanField()
    price_start = forms.IntegerField(label='Цена от', min_value=0)
    price_end = forms.IntegerField(label='Цена до', min_value=0)

    class Meta:
        model = Product
        fields = ('sex', 'breed', 'breed_type',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in self.fields:
            self.fields[field_name].required = False
