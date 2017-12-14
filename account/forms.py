from django import forms
from django.contrib.auth.models import User
from .models import Profile

from django.contrib.auth.forms import AuthenticationForm


class CustomLoginAuthForm(AuthenticationForm):
    username = forms.CharField(label='Nazwa użytkownika',
                               widget=forms.TextInput(
                                   attrs={'placeholder': 'Nazwa użytkownika'}))
    password = forms.CharField(label='Hasło',
                               widget=forms.PasswordInput(
                                   attrs={'placeholder': 'Hasło'}))


class UserRegistrationForm(forms.ModelForm):
    username = forms.CharField(label='Nazwa użytkownika',
                               widget=forms.TextInput(
                                   attrs={'placeholder': 'Nazwa użytkownika'}))
    password = forms.CharField(label='Hasło',
                               widget=forms.PasswordInput(
                                   attrs={'placeholder': 'Hasło'}))
    password2 = forms.CharField(label='Powtórz hasło',
                                widget=forms.PasswordInput(
                                    attrs={'placeholder': 'Powtórz hasło'}))

    class Meta:
        model = User
        fields = ('username',)

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Hasła nie są identyczne.')
        return cd['password2']
