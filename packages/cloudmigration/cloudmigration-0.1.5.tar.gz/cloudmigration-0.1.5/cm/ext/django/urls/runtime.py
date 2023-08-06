import importlib
import os
import sys
import inspect

from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from django.urls import include


assert 'CM_URLS_MODULE' in os.environ
self = sys.modules[__name__]
urls = importlib.import_module(os.environ['CM_URLS_MODULE'])
if not hasattr(urls, 'urlpatterns'):
    raise ValueError(
        "%s must declare urlpatterns" % os.environ['CM_SETTINGS_MODULE'])

urlpatterns = []
if getattr(settings, 'STATIC_SERVE', False):
    urlpatterns += static(settings.STATIC_URL,
        document_root=settings.STATIC_ROOT)


# Provide a configuration to enable or disable the
# Django Rest Framework API browser.
if getattr(settings, 'API_BROWSER_ENABLED', False)\
and 'rest_framework' in settings.INSTALLED_APPS:
    urlpatterns += [
        path(getattr(settings, 'API_BROWSER_PATH', 'browse/'),
            include('rest_framework.urls'))
    ]



urlpatterns.extend(urls.urlpatterns)

