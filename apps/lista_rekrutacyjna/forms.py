from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

class DodawanieRozmowy(forms.Form):
    imie = forms.CharField(label='Imię', max_length=100)
    nazwisko = forms.CharField(label='Nazwisko')
    data = forms.DateField(label='Data', widget=forms.TextInput(attrs={'id': 'datepicker'}))
    godzina = forms.TimeField(label='Godzina')

class LoginForm(forms.Form):
        user = forms.CharField(label='LOGIN')
        password = forms.CharField(label='HASŁO', widget=forms.PasswordInput)