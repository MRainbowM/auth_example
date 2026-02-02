from pathlib import Path

from environs import Env

env = Env()
env.read_env()

SECRET_KEY = env.str('SECRET_KEY')
DEBUG = env.bool('DEBUG', False)

ALLOWED_HOSTS = env.list(
    'ALLOWED_HOSTS',
    default=['localhost', '127.0.0.1', '0.0.0.0'],
)

CSRF_TRUSTED_ORIGINS = env.list(
    'CSRF_TRUSTED_ORIGINS',
    default=[
        'http://localhost',
        'http://127.0.0.1',
        'http://0.0.0.0',
        'http://localhost:8080',
        'http://127.0.0.1:8080',
        'http://0.0.0.0:8080',
    ],
)

BASE_DIR = Path(__file__).resolve().parent.parent.parent

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'apps.users.apps.UsersConfig',
    'apps.authentication.apps.AuthenticationConfig',
    'apps.authorization.apps.AuthorizationConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env('POSTGRES_DB', 'db'),
        'USER': env('POSTGRES_USER', 'user'),
        'PASSWORD': env('POSTGRES_PASSWORD', 'password'),
        'HOST': env('DB_HOST', 'localhost'),
        'PORT': env.int('DB_PORT', 5432),
    }
}

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'static_backend/'

ROOT_URLCONF = 'config.urls'

LANGUAGE_CODE = 'ru-ru'

TIME_ZONE = 'Asia/Shanghai'
