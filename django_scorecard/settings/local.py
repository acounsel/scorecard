from .base import *

DEBUG = True

ALLOWED_HOSTS = ['0.0.0.0', '.ngrok.io', 'localhost']

INSTALLED_APPS += ['debug_toolbar']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'scorecard',
        'USER': 'samer',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}