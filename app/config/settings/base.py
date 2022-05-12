"""Base settings to build other settings files upon."""

import environ

ROOT_DIR = environ.Path(__file__) - 3
APPS_DIR = ROOT_DIR.path('adminsmart')
FRONT_DIR = APPS_DIR.path('front')


env = environ.Env()

# Base
DEBUG = env.bool('DJANGO_DEBUG', False)

ALLOWED_HOSTS = [
	"*"
]

# Language and timezone
TIME_ZONE = 'America/Argentina/Salta'
LANGUAGE_CODE = 'es-ar'
SITE_ID = 1
USE_I18N = True
USE_L10N = True
USE_TZ = True

DATABASES = {
	'default': {
		'ENGINE': 'django.db.backends.postgresql',
		'NAME': env('POSTGRES_DB'),
		'USER': env('POSTGRES_USER'),
		'PASSWORD': env('POSTGRES_PASSWORD'),
		'HOST': env('POSTGRES_HOST'),
		'PORT': env('POSTGRES_PORT'),
	}
}


DATABASES['default']['ATOMIC_REQUESTS'] = True

# URLs
ROOT_URLCONF = 'config.urls'

# WSGI
WSGI_APPLICATION = 'config.wsgi.application'

# Users & Authentication
AUTH_USER_MODEL = 'users.User'

# Apps
DJANGO_APPS = [
	'django.contrib.auth',
	'django.contrib.contenttypes',
	'django.contrib.sessions',
	'django.contrib.messages',
	'django.contrib.staticfiles',
	'django.contrib.admin',
	'django.contrib.humanize',
	'django_afip',
	'corsheaders',
	'import_export'
]

THIRD_PARTY_APPS = [
	'rest_framework',
	'rest_framework.authtoken',
	'django_filters',
	'django_extensions'
]

LOCAL_APPS = [
	'adminsmart.apps.utils.apps.UtilsAppConfig',
	'adminsmart.apps.users.apps.UsersAppConfig',
	'adminsmart.apps.core.apps.OperativeAppConfig',
	'adminsmart.apps.platforms.apps.PlatformsAppConfig',
	'adminsmart.apps.files.apps.FilesAppConfig',
	'adminsmart.apps.platforms.expensas_pagas.apps.ExpensasPagasAppConfig',
	'adminsmart.apps.platforms.simple_solutions.apps.SimpleSolutionsAppConfig',
	'adminsmart.apps.communications.apps.CommunicationsAppConfig',
	'adminsmart.apps.informes.apps.InformesAppConfig',
	'adminsmart.api._public.apps.PublicAPIAppConfig',
	'adminsmart.front.apps.FrontendAppConfig'
]
INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

# Passwords
PASSWORD_HASHERS = [
	'django.contrib.auth.hashers.Argon2PasswordHasher',
	'django.contrib.auth.hashers.PBKDF2PasswordHasher',
	'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
	'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
	'django.contrib.auth.hashers.BCryptPasswordHasher',
]
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

# Middlewares
MIDDLEWARE = [
	'django.middleware.security.SecurityMiddleware',
	'django.middleware.common.CommonMiddleware',
	'django.middleware.csrf.CsrfViewMiddleware',
	'django.middleware.clickjacking.XFrameOptionsMiddleware',
	'django.contrib.sessions.middleware.SessionMiddleware',
	'django.contrib.auth.middleware.AuthenticationMiddleware',
	'django.contrib.messages.middleware.MessageMiddleware',
	'corsheaders.middleware.CorsMiddleware',

]

# Static files
STATIC_ROOT = str(ROOT_DIR('staticfiles'))
STATIC_URL = '/static/'
STATICFILES_DIRS = [
	str(APPS_DIR.path('static')),
]
STATICFILES_FINDERS = [
	'django.contrib.staticfiles.finders.FileSystemFinder',
	'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]

# Media
MEDIA_ROOT = str(ROOT_DIR('media'))
MEDIA_URL = '/media/'

# Templates
TEMPLATES = [
	{
		'BACKEND': 'django.template.backends.django.DjangoTemplates',
		'DIRS': [
			str(APPS_DIR.path('templates')),
			str(FRONT_DIR.path('templates')),
		],
		'OPTIONS': {
			'debug': DEBUG,
			'loaders': [
				'django.template.loaders.filesystem.Loader',
				'django.template.loaders.app_directories.Loader',
			],
			'context_processors': [
				'django.template.context_processors.debug',
				'django.template.context_processors.request',
				'django.contrib.auth.context_processors.auth',
				'django.template.context_processors.i18n',
				'django.template.context_processors.media',
				'django.template.context_processors.static',
				'django.template.context_processors.tz',
				'django.contrib.messages.context_processors.messages',
			],
		},
	},
]

# Security
SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_HTTPONLY = True
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = 'DENY'

# Email
DEFAULT_FROM_EMAIL = 'Equipo de AdminSmart <info@admin-smart.com>'

# Email con plantillas
# Creo que esto esta al pedo
TEMPLATED_EMAIL_BACKEND = 'templated_email.backends.vanilla_django.TemplateBackend'

# Admin
ADMIN_URL = 'dj-admin/'
ADMINS = [
	("Mariano Valdez", 'marianovaldez92@gmail.com'),
	("Agustin Ramos", 'ramosagustin2103@gmail.com'),
]
MANAGERS = ADMINS

# Cache
REDIS_URL = "redis://:{password}@{host}:{port}/0".format(
	password=env('REDIS_PASSWORD'),
	host=env('REDIS_HOST'),
	port=env('REDIS_PORT')
)
CACHES = {
	'default': {
		'BACKEND': 'django_redis.cache.RedisCache',
		'LOCATION': REDIS_URL,
		'OPTIONS': {
			'CLIENT_CLASS': 'django_redis.client.DefaultClient',
			'IGNORE_EXCEPTIONS': True,
		}
	}
}
# Celery
INSTALLED_APPS += ['adminsmart.taskapp.celery.CeleryAppConfig']
if USE_TZ:
	CELERY_TIMEZONE = TIME_ZONE
CELERY_BROKER_URL = REDIS_URL
CELERY_RESULT_BACKEND = REDIS_URL
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERYD_TASK_TIME_LIMIT = 5 * 60
CELERYD_TASK_SOFT_TIME_LIMIT = 60

# Django REST Framework
REST_FRAMEWORK = {
	'DEFAULT_RENDERER_CLASSES': (
		'rest_framework.renderers.JSONRenderer',
	),
	'DEFAULT_AUTHENTICATION_CLASSES': (
		'rest_framework.authentication.TokenAuthentication',
	),
	'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
	'PAGE_SIZE': 20000,
	'DEFAULT_FILTER_BACKENDS': ('django_filters.rest_framework.DjangoFilterBackend',),
	'DEFAULT_PARSER_CLASSES': [
		'rest_framework.parsers.JSONParser',
	],
	'COERCE_DECIMAL_TO_STRING': False,
}

CORS_ORIGIN_ALLOW_ALL = True


# Redireccion cuando el login no es correcto.
LOGIN_URL = '/login/'

# Redireccion cuando el login es correcto.
LOGIN_REDIRECT_URL = "/"
USER_ADMIN_LOGIN_REDIRECT = "cuentas-a-cobrar/"
USER_SOCIO_LOGIN_REDIRECT = "deudas/"

# Redireccion cuando el logout es correcto.
LOGOUT_REDIRECT_URL = '/login/'

