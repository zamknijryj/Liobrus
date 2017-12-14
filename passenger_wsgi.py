import sys
import os

sys.path.append(os.getcwd())
# zmienić 'nazwa_aplikacji' na
os.environ['DJANGO_SETTINGS_MODULE'] = "oceny_librus.settings"
# nazwę projektu Django

from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()
