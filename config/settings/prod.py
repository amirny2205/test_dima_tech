from .base import *

SECRET_KEY = env("SECRET_KEY")

DEBUG = False

ALLOWED_HOSTS = ["*"]

DATABASES = {
   'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': "",
        'USER': env("DATABASE_USER"),
        'PASSWORD': env("DATABASE_PASSWORD"),
        'HOST': "",
        'PORT': "",
   }
}

EMAIL_HOST = 'smtp.yandex.com'
EMAIL_PORT = '465'

# this is for the activation workaround. See "activation" function inside shop_main.views
SELF_HOST = 'http://localhost'
SELF_PORT = '8000'

PRIVATE_KEY = env('PRIVATE_KEY')
