from dotenv import load_dotenv

from .base import *

# macros
# docker run -d -it --rm --name memcached -p 11211:11211 memcached -m 64
# docker run -it -d --rm --name redis -p 6379:6379 redis

# python manage.py runserver --settings=educa.settings.local
print('educa.settings.local')

env_file = os.path.join(BASE_DIR.parent, '.local_dev.env')
load_dotenv(env_file)

SECRET_KEY = os.environ['SECRET_KEY']
DEBUG = True if os.environ.get('DEBUG', 0) == '1' else False

ALLOWED_HOSTS = os.environ['ALLOWED_HOSTS'].split(' ')

# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ['POSTGRES_DB'],
        'USER': os.environ['POSTGRES_USER'],
        'PASSWORD': os.environ['POSTGRES_PASSWORD'],
        'HOST': os.environ['POSTGRES_HOST'],
        'PORT': os.environ['POSTGRES_PORT'],
    }
}

REDIS_PREFIX = os.environ['REDIS_PREFIX']
REDIS_HOST = os.environ['REDIS_HOST']
REDIS_PORT = os.environ['REDIS_PORT']
REDIS_URL = f"{REDIS_PREFIX}://{REDIS_HOST}:{REDIS_PORT}"

CACHES['default']['LOCATION'] = REDIS_URL
CHANNEL_LAYERS['CONFIG']['hosts'] = [(REDIS_HOST, REDIS_PORT), ]
