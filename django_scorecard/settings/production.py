from .base import *

DEBUG = True

ALLOWED_HOSTS = ['cryptic-falls-54884.herokuapp.com']

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