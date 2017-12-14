from django.contrib import auth
from django.contrib.auth import authenticate, login
from rest_framework import generics, views
from rest_framework.response import Response

from librus.librus import LibrusOceny

from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from datetime import date, timedelta, datetime

from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from .serializers import *
from account.models import (
    Sprawdzian,
    PracaKlasowa,
    Profile,)

from django.contrib.auth.models import User


class SprawdzianAPIData(generics.ListAPIView):
    serializer_class = SprawdzianListSerializer

    def get_queryset(self):
        current_user = self.request.user
        return Sprawdzian.objects.filter(user=current_user)


class PraceKlasoweAPIData(generics.ListAPIView):
    serializer_class = PracaKlasowaListSerializer

    def get_queryset(self):
        current_user = self.request.user
        return PracaKlasowa.objects.filter(user=current_user)


class WiadomosciListAPIData(generics.ListAPIView):
    serializer_class = WiadomosciListSerializer

    def get_queryset(self):
        current_user = self.request.user

        return Wiadomosc.objects.filter(user=current_user)


class WiadomosciDetailAPI(generics.RetrieveAPIView):
    serializer_class = WiadomosciListSerializer
    
    def get_queryset(self):
        current_user = self.request.user

        return Wiadomosc.objects.filter(user=current_user)


class UserAPIData(generics.ListAPIView):
    serializer_class = UserAPISerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        current_user = self.request.user
        return Profile.objects.filter(user=current_user)


class AktualizacjaAPI(views.APIView):
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)

    serializer_class = AktualizacjaSerializer

    def get_queryset(self):
        return Profile.objects.filter(user=self.request.user)

    def post(self, request, *args, **kwargs):
        data = request.data

        if data['librus_user'] == "fake" and data['librus_pswd'] == 'fakePassword':

            data_response = {
                "done": True
            }

            return Response(data_response)

        else:

            lib = LibrusOceny()
            lib.connectToLibrus(data['librus_user'], data['librus_pswd'])
            oceny = lib.oceny_skon
            imie = lib.getUserName()
            szczesliwy_numerek = lib.numerek
            numerek_dzien = lib.numerek_dzien
            klasa = lib.klasaUcznia()
            numerek_w_dzien = lib.numerUcznia()

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

            Profile.objects.filter(user=request.user).update(
                imie=imie,
                klasa=klasa,
                num_w_dzienniku=numerek_w_dzien,
                oceny=oceny_display,
                srednia=srednia,
                szczesliwy_numerek=szczesliwy_numerek,
                data_numerka=numerek_dzien,
                login=data['librus_user'],
                passwd=data['librus_pswd']
            )

            data_response = {
                "Done": True
            }
            return Response(data_response)


class UserLoginAPI(views.APIView):
    authentication_classes = (SessionAuthentication, BasicAuthentication)

    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        data = request.data  # request.POST
        serializer = UserLoginSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            new_data = serializer.data
            user = authenticate(
                username=new_data['username'], password=new_data['password'])
            login(request, user)
            return Response(new_data, status=HTTP_200_OK)
        new_data = {
            'xd': 10
        }
        return Response(new_data)


class UserCreateAPI(generics.CreateAPIView):
    serializer_class = UserCreateSerializer
    queryset = User.objects.all()

    def perform_create(self, serializer):
        instance = serializer.save()
        instance.set_password(instance.password)
        instance.save()
        info = 'Zaktualizuj dane, aby zobaczyć wynik.'
        Profile.objects.create(user=instance,
                               imie=info,
                               oceny=info,
                               srednia=info,
                               data_numerka=info)


class ChartData(views.APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        current_user = auth.get_user(request)  # get current user
        oceny = current_user.profile.oceny
        labels = ['0', "1", "2", "3", "4", "5", "6"]
        zero = oceny.count('0')
        jeden = oceny.count('1')
        dwa = oceny.count('2')
        trzy = oceny.count('3')
        cztery = oceny.count('4')
        piec = oceny.count('5')
        szesc = oceny.count('6')
        oceny_data = [zero, jeden, dwa, trzy, cztery, piec, szesc]
        data = {
            'labels': labels,
            'default': oceny_data,
            'max': max(oceny_data) + 1
        }
        return Response(data)
