from django.contrib.auth.urls import url
from . import views
from .views import *


urlpatterns = [
    url(r'^$', views.aktualizacjaAutomatyczna, name='home'),
    url(r'^aktualizacja/$', views.aktualizacja, name='aktualizacja'),
    url(r'^sprawdziany/$', LibrusSprawdziany.as_view(), name='terminarz'),
    url(r'^prace-klasowe/$', LibrusPraceKlasowe.as_view(), name='prace-klasowe'),
    url(r'^wiadomosci/$', WiadomosciList.as_view(), name='wiadomosci'),
    url(r'^wiadomosc/(?P<pk>\d+)/$', WidomosciDetail.as_view(), name='wiadomosc_detail'),
]
