from django import forms
from .models import Oceny


class LibrusForm(forms.ModelForm):
    login = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Nazwa użytkownika Librus'}),
                            label='Nazwa użytkownika Librus')
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Hasło'}),
                               label='Hasło')

    class Meta:
        model = Oceny
        exclude = ('oceny', 'test')


class LibrusTest(forms.ModelForm):

    class Meta:
        model = Oceny
        exclude = ['oceny', 'test']


