"""Base settings to build other settings files upon."""

import environ

ROOT_DIR = environ.Path(__file__) - 3
APPS_DIR = ROOT_DIR


env = environ.Env()

# Base
DEBUG = env.bool('DJANGO_DEBUG', False)
SECRET_KEY = 'PB3aGvTmCkzaLGRAxDc3aMayKTPTDd5usT8gw4pCmKOk5AlJjh12pTrnNgQyOHCH'


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
		'ENGINE': 'django.db.backends.mysql',
		'HOST': env('DDBB_HOST', default=None),
		'PORT': env('DDBB_PORT', default=None),
		'NAME': env('DDBB_NAME', default=None),
		'USER': env('DDBB_USER', default=None),
		'PASSWORD': env('DDBB_PASSWORD', default=None),
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
	'utils.apps.UtilsAppConfig',
	'users.apps.UsersAppConfig',
	'core.apps.OperativeAppConfig',
	'communications.apps.CommunicationsAppConfig',
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
	'django.middleware.gzip.GZipMiddleware',
	'django.contrib.sessions.middleware.SessionMiddleware',
	'django.contrib.auth.middleware.AuthenticationMiddleware',
	'django.contrib.messages.middleware.MessageMiddleware',
	'corsheaders.middleware.CorsMiddleware',

]

# Static files
STATIC_ROOT = str(ROOT_DIR('staticfiles'))
STATIC_URL = '/static/'
STATICFILES_DIRS = []

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
			str(APPS_DIR.path('/app/templates')),
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
EMAIL_BACKEND = env('EMAIL_BACKEND', default='django.core.mail.backends.console.EmailBackend')
EMAIL_HOST = env('EMAIL_HOST', default='172.21.0.1')
EMAIL_PORT = env('EMAIL_PORT', default=25)
EMAIL_USE_TLS = env('EMAIL_USE_TLS', default=False)
EMAIL_USE_SSL = env('EMAIL_USE_SSL', default=False)
DEFAULT_FROM_EMAIL = env('DJANGO_DEFAULT_FROM_EMAIL', default='AdminOrg <info@adminorg.com.ar>')
SERVER_EMAIL = env('DJANGO_DEFAULT_FROM_EMAIL', default=DEFAULT_FROM_EMAIL)


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


# Django REST Framework
REST_FRAMEWORK = {
	'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
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

# Redireccion cuando el logout es correcto.
LOGOUT_REDIRECT_URL = '/login/'

REACT = {
    'core': 'assets/js/react/react.development.js',
    'dom': 'assets/js/react/react-dom.development.js',
    'babel': 'assets/js/react/babel.min.js'
}



LOGGING = {
	'version': 1,
	'disable_existing_loggers': False,
	'filters': {
		'require_debug_false': {
			'()': 'django.utils.log.RequireDebugFalse'
		}
	},
	'formatters': {
		'verbose': {
			'format': '%(levelname)s %(asctime)s %(module)s '
					  '%(process)d %(thread)d %(message)s'
		},
	},
	'handlers': {
		'mail_admins': {
			'level': 'ERROR',
			'filters': ['require_debug_false'],
			'class': 'django.utils.log.AdminEmailHandler'
		},
		'console': {
			'level': 'DEBUG',
			'class': 'logging.StreamHandler',
			'formatter': 'verbose',
		},
	},
	'loggers': {
		'django.request': {
			'handlers': ['mail_admins'],
			'level': 'ERROR',
			'propagate': True
		},
		'django.security.DisallowedHost': {
			'level': 'ERROR',
			'handlers': ['console', 'mail_admins'],
			'propagate': True
		}
	}
}