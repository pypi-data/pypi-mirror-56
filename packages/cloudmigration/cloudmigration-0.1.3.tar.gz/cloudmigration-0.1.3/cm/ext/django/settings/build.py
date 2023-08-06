"""Django settings used during a container build; used
mainly to support ``collectstatic``.
"""
from cm.ext.django.settings.const import *

DEBUG = False

SECRET_KEY = ('0' * 32)
