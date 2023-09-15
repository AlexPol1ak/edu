import os

from dotenv import load_dotenv

from .base import *

env_file = os.path.join(BASE_DIR.parent, '.local_dev.env')
# env_file = os.path.join(BASE_DIR.parent, '.vps.env')
load_dotenv(env_file)

SECRET_KEY = os.environ['SECRET_KEY']
DEBUG = True if os.environ['DEBUG'] == '1' else False

ADMINS = [(os.environ['ADMIN_NAME'], os.environ['ADMIN_EMAIL'])]
ALLOWED_HOSTS = os.environ['ALLOWED_HOSTS'].split(' ')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ['POSTGRES_DB'],
        'USER': os.environ['POSTGRES_USER'],
        'PASSWORD': os.environ['POSTGRES_PASSWORD'],
        'HOST': os.environ['POSTGRES_HOST'],
        'PORT': os.environ['POSTGRES_PORT'],
        'CONN_MAX_AGE': int(os.environ['CONN_MAX_AGE']),
    }
}


REDIS_PREFIX = os.environ['REDIS_PREFIX']
REDIS_HOST = os.environ['REDIS_HOST']
REDIS_PORT = os.environ['REDIS_PORT']
REDIS_URL = f"{REDIS_PREFIX}://{REDIS_HOST}:{REDIS_PORT}"

CACHES['default']['LOCATION'] = REDIS_URL
CHANNEL_LAYERS['default']['CONFIG'] = {'hosts': [REDIS_URL]}

CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = True


