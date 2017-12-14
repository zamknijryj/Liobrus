from django.contrib.auth.urls import url
from .views import *

urlpatterns = [
    url(r'^sprawdzian/data/$', SprawdzianAPIData.as_view()),
    url(r'^praca-klasowa/data/$', PraceKlasoweAPIData.as_view()),
    url(r'^user/data/$', UserAPIData.as_view()),
    url(r'^user/data/aktualizacja/$', AktualizacjaAPI.as_view()),
    url(r'^chart/data/$', ChartData.as_view()),
    url(r'^user/login/$', UserLoginAPI.as_view()),
    url(r'^user/register/$', UserCreateAPI.as_view()),
    url(r'^wiadomosci/data/$', WiadomosciListAPIData.as_view()),
    url(r'^wiadomosci/(?P<pk>[\d]+)/$', WiadomosciDetailAPI.as_view())
]
