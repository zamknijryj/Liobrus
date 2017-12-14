from django.contrib import admin
from .models import (
    Profile,
    Sprawdzian,
    PracaKlasowa,
    Wiadomosc
)


class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'imie', 'klasa', 'updated']
    list_filter = ['imie', 'klasa', 'num_w_dzienniku']
    search_fields = ['przedmiot', 'opis']


class SprawdzianAdmin(admin.ModelAdmin):
    list_display = ['rodzaj', 'user', 'przedmiot', 'nauczyciel', 'data']
    list_filter = ['rodzaj', 'user', 'przedmiot', 'data', 'nauczyciel']
    search_fields = ['przedmiot', 'opis']


class PracaKlasowaAdmin(admin.ModelAdmin):
    list_display = ['rodzaj', 'user', 'przedmiot', 'nauczyciel', 'data']
    list_filter = ['rodzaj', 'user', 'przedmiot', 'nauczyciel', 'data']
    search_fields = ['przedmiot', 'opis']


admin.site.register(Profile, ProfileAdmin)
admin.site.register(Sprawdzian, SprawdzianAdmin)
admin.site.register(PracaKlasowa, PracaKlasowaAdmin)
admin.site.register(Wiadomosc)
