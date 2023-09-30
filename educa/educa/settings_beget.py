import os
from pathlib import Path
from django.urls import reverse_lazy
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

env_file = os.path.join(BASE_DIR.parent, '.beget.env')
load_dotenv(env_file)

# load_dotenv()

SECRET_KEY = os.environ['SECRET_KEY']
DEBUG = True if os.environ['DEBUG'] == '1' else False

print(f"{'*' * 25}\n Load {os.environ['ENV_NAME']}\n{'*' * 25}\nDEBUG={DEBUG}\n{'*' * 25}\n")

# Disclose on deposition
ALLOWED_HOSTS = os.environ['ALLOWED_HOSTS'].split(' ')

URLS_TRUSTED_ORIGINS = os.environ['CSRF_TRUSTED_ORIGINS'].split(' ')
CSRF_TRUSTED_ORIGINS = []
for url in URLS_TRUSTED_ORIGINS:
    CSRF_TRUSTED_ORIGINS.extend(['https://'+url, 'http://'+url])
print(CSRF_TRUSTED_ORIGINS)

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'courses.apps.CoursesConfig',
    'students.apps.StudentsConfig',
    'chat',
    'embed_video',
    'debug_toolbar',
    'redisboard',
    'rest_framework',
    'channels',
    'daphne',
]

MIDDLEWARE = [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'educa.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ['MYSQL_DB'],
        'USER': os.environ['MYSQL_USER'],
        'PASSWORD': os.environ['MYSQL_PASSWORD'],
        'CONN_MAX_AGE': int(os.environ['CONN_MAX_AGE']),
        'HOST': os.environ['MYSQL_HOST'],
        'PORT': os.environ['MYSQL_PORT'],
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATICFILES_DIRS = [
    (os.path.join(BASE_DIR, "courses/static")),
]

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
LOGIN_REDIRECT_URL = reverse_lazy('student_course_list')
LOGOUT_REDIRECT_URL = reverse_lazy('student_registration')

REDIS_PREFIX = os.environ['REDIS_PREFIX']
REDIS_HOST = os.environ['REDIS_HOST']
REDIS_PORT = os.environ['REDIS_PORT']
REDIS_URL = f"{REDIS_PREFIX}://{REDIS_HOST}:{REDIS_PORT}"

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly',
    ],
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': REDIS_URL,
    },

}

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {'hosts': [(REDIS_HOST, int(REDIS_PORT))]},
    },

}

WSGI_APPLICATION = 'educa.wsgi.application'
ASGI_APPLICATION = 'educa.asgi.application'

INTERNAL_IPS = ['127.0.0.1']

# Disclose on deposition
# CSRF_COOKIE_SECURE = True
# SESSION_COOKIE_SECURE = True
# SECURE_SSL_REDIRECT = True
