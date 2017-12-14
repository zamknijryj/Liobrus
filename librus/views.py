from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import generic
from .forms import LibrusForm, LibrusTest
from account.models import (
    Sprawdzian,
    PracaKlasowa,
    Wiadomosc
)
from .librus import LibrusOceny

from datetime import date, timedelta, datetime


@login_required
def aktualizacja(request):
    if request.method == 'POST':
        form = LibrusForm(data=request.POST, instance=request.user.profile)
        if form.is_valid():
            username = form.cleaned_data['login']
            password = form.cleaned_data['password']

            lib = LibrusOceny()
            lib.connectToLibrus(username, password)
            oceny = lib.oceny_skon
            imie = lib.getUserName()
            szczesliwy_numerek = lib.numerek
            numerek_dzien = lib.numerek_dzien
            klasa = lib.klasaUcznia()
            numerek_w_dzien = lib.numerUcznia()
            liczba_spr = len(lib.full_links)

            full_spr = lib.full_spr
            Sprawdzian.objects.filter(user=request.user).delete()
            this_day = date.today() + timedelta(days=1)
            for spr in full_spr:
                sprawdzian = Sprawdzian.objects.create(
                    user=request.user,
                    data=spr['Data'],
                    nr_lekcji=spr['Nr lekcji'],
                    nauczyciel=spr['Nauczyciel'],
                    rodzaj=spr['Rodzaj'],
                    przedmiot=spr['Przedmiot'],
                    opis=spr['Opis'],
                    data_dodania=spr['Data dodania']
                )
                # print(sprawdzian.data)
                # print(this_day)
                data_sprawdzianu = datetime.strptime(
                    sprawdzian.data, "%Y-%m-%d").date()
                if data_sprawdzianu > this_day:
                    pass
                else:
                    sprawdzian.delete()

            # PRACE KLASOWE

            prace_kl = lib.prace
            PracaKlasowa.objects.filter(user=request.user).delete()
            for praca in prace_kl:
                praca_klasowa = PracaKlasowa.objects.create(
                    user=request.user,
                    data=praca['Data'],
                    nr_lekcji=praca['Nr lekcji'],
                    nauczyciel=praca['Nauczyciel'],
                    rodzaj=praca['Rodzaj'],
                    przedmiot=praca['Przedmiot'],
                    opis=praca['Opis'],
                    data_dodania=praca['Data dodania']
                )
                # print(praca_klasowa.data)
                data_pracy = datetime.strptime(
                    praca_klasowa.data, "%Y-%m-%d").date()
                if data_pracy > this_day:
                    pass
                else:
                    praca_klasowa.delete()

            oceny_display = ', '.join(oceny)
            srednia = lib.sredniaArytmetyczna(lib.oceny2)
            srednia = round(srednia, 2)

            post = form.save(commit=False)
            post.user = request.user
            post.imie = imie
            post.klasa = klasa
            post.num_w_dzienniku = numerek_w_dzien
            post.oceny = oceny_display
            post.srednia = srednia
            post.szczesliwy_numerek = szczesliwy_numerek
            post.data_numerka = numerek_dzien
            post.login = username
            post.passwd = password
            post.save()
            messages.success(
                request, 'Dane zostały zaktualizowane, dziękujemy!')
            context = {'form': form, }
            return redirect('home')
    else:
        form = LibrusForm(instance=request.user.profile)
    context = {'form': form}
    return render(request, 'librus/aktualizacja.html', context)


@login_required
def aktualizacjaAutomatyczna(request):
    if request.method == 'POST':
        form = LibrusTest(data=request.POST, instance=request.user.profile)
        if form.is_valid():
            username = request.user.profile.login
            password = request.user.profile.passwd

            lib = LibrusOceny()
            lib.connectToLibrus(username, password)
            oceny = lib.oceny_skon
            imie = lib.getUserName()
            szczesliwy_numerek = lib.numerek
            numerek_dzien = lib.numerek_dzien
            klasa = lib.klasaUcznia()
            numerek_w_dzien = lib.numerUcznia()

            full_spr = lib.full_spr
            Sprawdzian.objects.filter(user=request.user).delete()
            this_day = date.today()
            for spr in full_spr:
                sprawdzian = Sprawdzian.objects.create(
                    user=request.user,
                    data=spr['Data'],
                    nr_lekcji=spr['Nr lekcji'],
                    nauczyciel=spr['Nauczyciel'],
                    rodzaj=spr['Rodzaj'],
                    przedmiot=spr['Przedmiot'],
                    opis=spr['Opis'],
                    data_dodania=spr['Data dodania']
                )
                # print(sprawdzian.data)
                # print(this_day)
                data_sprawdzianu = datetime.strptime(
                    sprawdzian.data, "%Y-%m-%d").date()
                if data_sprawdzianu > this_day:
                    pass
                else:
                    sprawdzian.delete()

            # PRACE KLASOWE
            prace_kl = lib.prace
            PracaKlasowa.objects.filter(user=request.user).delete()
            for praca in prace_kl:
                praca_klasowa = PracaKlasowa.objects.create(
                    user=request.user,
                    data=praca['Data'],
                    nr_lekcji=praca['Nr lekcji'],
                    nauczyciel=praca['Nauczyciel'],
                    rodzaj=praca['Rodzaj'],
                    przedmiot=praca['Przedmiot'],
                    opis=praca['Opis'],
                    data_dodania=praca['Data dodania']
                )
                # print(praca_klasowa.data)
                data_pracy = datetime.strptime(
                    praca_klasowa.data, "%Y-%m-%d").date()
                if data_pracy > this_day:
                    pass
                else:
                    praca_klasowa.delete()

            wiadomosci = lib.wiadomosci()
            Wiadomosc.objects.filter(user=request.user).delete()
            for wid in wiadomosci:
                wiad = Wiadomosc.objects.create(
                    user=request.user,
                    nadawca=wid['Nadawca'],
                    temat=wid['Temat'],
                    wiadomosc=wid['Widaomośc'],
                    data_wyslania=wid['Wysłano']
                )

            oceny_display = ', '.join(oceny)
            srednia = lib.sredniaArytmetyczna(lib.oceny2)
            srednia = round(srednia, 2)

            post = form.save(commit=False)
            post.user = request.user
            post.imie = imie
            post.klasa = klasa
            post.num_w_dzienniku = numerek_w_dzien
            post.oceny = oceny_display
            post.srednia = srednia
            post.szczesliwy_numerek = szczesliwy_numerek
            post.data_numerka = numerek_dzien
            post.login = username
            post.passwd = password
            post.save()
            messages.success(
                request, 'Dane zostały zaktualizowane, dziękujemy!')
            context = {'form': form, }
            return redirect('home')
    else:
        form = LibrusTest(instance=request.user.profile)
    context = {'form': form}
    return render(request, 'librus/librus.html', context)


@method_decorator(login_required, name='dispatch')
class LibrusMain(generic.TemplateView):
    template_name = 'librus/librus.html'

    def get_context_data(self, **kwargs):
        context = super(LibrusMain, self).get_context_data(**kwargs)
        context['section'] = 'home'
        return context


@method_decorator(login_required, name='dispatch')
class LibrusSprawdziany(generic.ListView):
    template_name = 'librus/sprawdziany.html'
    model = Sprawdzian

    def get_context_data(self, **kwargs):
        context = super(LibrusSprawdziany, self).get_context_data(**kwargs)
        context['liczba_spr'] = Sprawdzian.objects.filter(
            user=self.request.user).count()
        this_day = date.today()
        try:
            first_test = Sprawdzian.objects.filter(
                user=self.request.user).first().data
        except AttributeError:
            pass

        try:
            context['do_testu'] = "Do najbliższego sprawdzainu zostało: {}".format(
                first_test - this_day)
        except:
            context['do_testu'] = 'BRAK SPRAWDZIANÓW'
        context['section'] = 'sprawdziany'
        context['prace_list'] = PracaKlasowa.objects.filter(
            user=self.request.user)
        return context

    def get_queryset(self):
        object_list = Sprawdzian.objects.filter(user=self.request.user)

        return object_list


@method_decorator(login_required, name='dispatch')
class WiadomosciList(generic.ListView):
    template_name = 'librus/wiadomosci.html'
    model = Wiadomosc

    def get_context_data(self, **kwargs):

        context = super(WiadomosciList, self).get_context_data(**kwargs)

        context['section'] = 'wiadomosci'
        context['liczba_wiad'] = Wiadomosc.objects.count()

        return context

    def get_queryset(self):
        object_list = Wiadomosc.objects.filter(user=self.request.user)

        return object_list


@method_decorator(login_required, name='dispatch')
class WidomosciDetail(generic.DetailView):
    template_name = 'librus/wiadomosc_detail.html'
    model = Wiadomosc

@method_decorator(login_required, name='dispatch')
class LibrusPraceKlasowe(generic.ListView):
    template_name = 'librus/prace_klasowe.html'
    model = PracaKlasowa

    def get_context_data(self, **kwargs):

        this_day = date.today()
        try:
            pierwsza_praca = PracaKlasowa.objects.filter(
                user=self.request.user).first().data
        except AttributeError:
            pass

        context = super(LibrusPraceKlasowe, self).get_context_data(**kwargs)
        context['liczba_prac'] = PracaKlasowa.objects.filter(
            user=self.request.user).count()
        context['section'] = 'praca_klasowa'
        try:
            context['do_pracy'] = "Do najbliższej pracy klasowej zostało: {}".format(
                pierwsza_praca - this_day)
        except:
            context['do_pracy'] = 'BRAK PRAC KLASOWYCH'

        return context

    def get_queryset(self):
        object_list = PracaKlasowa.objects.filter(user=self.request.user)

        return object_list


def custom_404(request):
    return render(request, '404.html', status=404)


def custom_500(request):
    return render(request, '500.html')
