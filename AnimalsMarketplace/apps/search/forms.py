from django import forms


class SearchForm(forms.Form):
    q = forms.CharField(
        widget=forms.TextInput(attrs={'id': "autoComplete", 'autocomplete': 'off', 'class': 'form-control',
                                      'style': 'height:42px;', 'placeholder': "Поиск по названию и описанию"}))
