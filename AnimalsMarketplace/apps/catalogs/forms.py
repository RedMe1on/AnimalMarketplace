from django import forms
from .models import Product, RatingProduct
from django.db.utils import ProgrammingError as AvoidDataMigrationError


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
    image = forms.BooleanField()
    price_start = forms.IntegerField(label='Цена от')
    price_end = forms.IntegerField(label='Цена до')

    class Meta:
        model = Product
        fields = ('sex', 'breed', 'breed_type',)
        # При миграциях возникает ошибка из-за того, что идет вызов из базы данных из файла form, а не view
        # Поэтому ловим эту ошибку и пропускаем, т.к. все будет работать
        try:
            widgets = {
                'sex': forms.SelectMultiple(
                    attrs={'class': 'selectpicker filter-input', 'title': 'Пол', 'data-style': 'filter-input'},
                    choices=Product.SexChoices.choices),
                'breed': forms.SelectMultiple(
                    attrs={'class': 'selectpicker filter-input', 'title': 'Порода', 'data-style': 'filter-input'},
                    choices=Product.BreedChoices.choices),
                'breed_type': forms.SelectMultiple(
                    attrs={'class': 'selectpicker filter-input', 'title': 'Вид породы', 'data-size': '5',
                           'data-live-search': 'true', 'data-style': 'filter-input'},
                    choices=[(product.breed_type, product.breed_type) for product in
                             Product.objects.order_by('breed_type').distinct(
                                 'breed_type')]),

            }
        except AvoidDataMigrationError:
            pass

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in self.fields:
            self.fields[field_name].required = False
