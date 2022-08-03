"""Production settings."""

from .base import *  # NOQA

# Base
SECRET_KEY = env('DJANGO_SECRET_KEY', default='PB3aGvTmCkzaLGRAxDc3aMayKTPTDd5usT8gw4pCmKOk5AlJjh12pTrnNgQyOHCH')
# Gunicorn
INSTALLED_APPS += ['gunicorn']  # noqa F405

# Databases
DATABASES['default']['ATOMIC_REQUESTS'] = True  # NOQA
# DATABASES['default']['CONN_MAX_AGE'] = env.int('CONN_MAX_AGE', default=60)  # NOQA
# DATABASES['default']['OPTIONS'] = {'sslmode': 'require'}

# Security
# SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
# SECURE_SSL_REDIRECT = env.bool('DJANGO_SECURE_SSL_REDIRECT', default=True)
# SESSION_COOKIE_SECURE = True
# CSRF_COOKIE_SECURE = True
# SECURE_HSTS_SECONDS = 60
# SECURE_HSTS_INCLUDE_SUBDOMAINS = env.bool('DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS', default=True)
# SECURE_HSTS_PRELOAD = env.bool('DJANGO_SECURE_HSTS_PRELOAD', default=True)
# SECURE_CONTENT_TYPE_NOSNIFF = env.bool('DJANGO_SECURE_CONTENT_TYPE_NOSNIFF', default=True)

# Storages
INSTALLED_APPS += ['storages']  # noqa F405
AWS_ACCESS_KEY_ID = "AKIA44JZ4ACAULPKDEWP"
AWS_SECRET_ACCESS_KEY = "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"
AWS_STORAGE_BUCKET_NAME = 'adminsmart.files'
AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME
AWS_S3_CUSTOM_DOMAIN = "d3dmzz5192bnwx.cloudfront.net"
AWS_DEFAULT_ACL = None
AWS_QUERYSTRING_AUTH = False
_AWS_EXPIRY = 60 * 60 * 24 * 7
AWS_S3_OBJECT_PARAMETERS = {
	'CacheControl': f'max-age={_AWS_EXPIRY}, s-maxage={_AWS_EXPIRY}, must-revalidate',
}

# Static  files
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
AWS_STATIC_LOCATION = 'static'
STATIC_URL = 'https://%s/%s/' % (AWS_S3_CUSTOM_DOMAIN, AWS_STATIC_LOCATION)

# # Media
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
AWS_MEDIA_LOCATION = 'media'
MEDIA_URL = 'https://%s/%s/' % (AWS_S3_CUSTOM_DOMAIN, AWS_MEDIA_LOCATION)

# Templates
TEMPLATES[0]['OPTIONS']['loaders'] = [  # noqa F405
	(
		'django.template.loaders.cached.Loader',
		[
			'django.template.loaders.filesystem.Loader',
			'django.template.loaders.app_directories.Loader',
		]
	),
]

# Email
DEFAULT_FROM_EMAIL = env(
	'DJANGO_DEFAULT_FROM_EMAIL',
	default='AdminSmart <info@admin-smart.com>'
)
SERVER_EMAIL = env('DJANGO_SERVER_EMAIL', default=DEFAULT_FROM_EMAIL)
EMAIL_SUBJECT_PREFIX = env('DJANGO_EMAIL_SUBJECT_PREFIX', default='[AdminSmart]')

# Email
EMAIL_HOST = 'smtp.mailgun.org'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'postmaster@mail.admin-smart.com'
EMAIL_HOST_PASSWORD = '7696916e7d3a29748757b17f82f9924a-30b9cd6d-a50b7d8e'
EMAIL_USE_TLS = True


# WhiteNoise
# MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')  # noqa F405


# Logging
# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See https://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
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
DEBUG = True

REACT = {
    'core': 'assets/js/react/react.production.min.js',
    'dom': 'assets/js/react/react-dom.production.min.js',
    'babel': 'assets/js/react/babel.min.js'
}

import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

sentry_sdk.init(
	dsn="https://87bd862b6e0e43c881b9059f5920918a@o1151668.ingest.sentry.io/6228979",
	integrations=[DjangoIntegration()],

	# Set traces_sample_rate to 1.0 to capture 100%
	# of transactions for performance monitoring.
	# We recommend adjusting this value in production,
	traces_sample_rate=1.0,

	# If you wish to associate users to errors (assuming you are using
	# django.contrib.auth) you may enable sending PII data.
	send_default_pii=True,

	# By default the SDK will try to use the SENTRY_RELEASE
	# environment variable, or infer a git commit
	# SHA as release, however you may want to set
	# something more human-readable.
	# release="myapp@1.0.0",
)