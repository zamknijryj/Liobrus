from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .models import Profile, Sprawdzian
from .forms import UserRegistrationForm


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Utworzenie nowego obiektu użytkownika,
            # ale jeszcze nie zapisujemy go w bazie danych.
            new_user = user_form.save(commit=False)
            # Ustawienie wybranego hasła.
            new_user.set_password(
                user_form.cleaned_data['password'])
            # Zapisanie obiektu User.

            new_user.save()
            # Utworzenie profilu użytkownika.
            info = 'Zaktualizuj dane, aby zobaczyć wynik.'
            profile = Profile.objects.create(user=new_user,
                                             imie=info,
                                             oceny=info,
                                             srednia=info,
                                             data_numerka=info)
            nazwa = user_form.cleaned_data['username']
            haslo = user_form.cleaned_data['password']

            user = authenticate(username=nazwa, password=haslo)

            login(request, user)

            messages.success(
                request, 'Konto zostało założone, zaktualizuj dane, aby zobaczyć wynik.')
            return redirect('home')
    else:
        user_form = UserRegistrationForm()
    return render(request,
                  'account/register.html',
                  {'user_form': user_form})
