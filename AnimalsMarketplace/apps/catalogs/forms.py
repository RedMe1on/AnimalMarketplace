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

# class OwnerLoginForm(LoginForm):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         # for fieldname, field in self.fields.items():
#         #     field.widget.attrs.update({
#         #         'class': 'form-control-plaintext'
#         #     })
#
#
# class OwnerSignupForm(SignupForm):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
# self.fields['new'] = forms.CharField(required=True)
# for fieldname, field in self.fields.items():
#     field.widget.attrs.update({
#         'class': 'form-control-plaintext'
#     })
