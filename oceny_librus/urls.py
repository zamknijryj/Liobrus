from django.conf.urls import url, include
from django.contrib import admin
from librus import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include('librus.urls')),
    url(r'^account/', include('account.urls')),
    url(r'^api/', include('librus.api.urls')),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)

handler404 = views.custom_404
handler500 = views.custom_500
