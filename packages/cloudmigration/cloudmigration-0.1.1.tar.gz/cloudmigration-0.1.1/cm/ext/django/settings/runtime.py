import importlib
import os
import sys
import inspect

import yaml

import cm.lib.environ


__all__ = []

assert 'CM_SETTINGS_MODULE' in os.environ


# Retrieve the current module from the sys.modules dictionary;
# we can then dynamically copy over settings from the real
# Django settings module.
self = sys.modules[__name__]
base_settings = importlib.import_module(os.environ['CM_SETTINGS_MODULE'])


# Iterate over all attributes in the original settings module
# and set them as attributes.
for attname, value in inspect.getmembers(base_settings):
    setattr(self, attname, value)


# The following settings are hard-coded and needed for proper
# deployment on the CM platform.
STATIC_ROOT = 'static'

STATICFILES_DIRS = ['dist/assets']


# Below members are operational configurations that are enforced
# by the CM platform. Since they are mandatory for deployment,
# we have the assignments raise an exception if the keys do
# not exist.
ALLOWED_HOSTS = cm.lib.environ.parselist(os.environ,
    'HTTP_ALLOWED_HOSTS', sep=';')

DEBUG = os.getenv('DEBUG') == '1'

SECRET_KEY = os.getenv('SECRET_KEY') or ('0' * 32)

STATIC_URL = os.getenv('STATIC_URL') or '/assets/'
if not str.endswith(STATIC_URL, '/'):
    STATIC_URL = STATIC_URL + '/'


# We check here if DEBUG is True and the SECRET_KEY consist
# of all zeroes, to prevent insecure keys getting deployed
# in a production environment.
if not DEBUG and SECRET_KEY == ('0' * 32):
    raise RuntimeError("Insecure SECRET_KEY configured.")
