from django.contrib.auth.urls import url
from django.contrib.auth.views import (
    logout,
    login
)
from .views import (
    register
)
from .forms import CustomLoginAuthForm

urlpatterns = [
    url(r'^login/$', login, name='login',
        kwargs={"authentication_form": CustomLoginAuthForm}),
    url(r'^register/$', register, name="register"),
    url(r'^logout/$', logout, name='logout'),
]
