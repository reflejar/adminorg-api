#!/bin/sh

set -o errexit
set -o pipefail
set -o nounset

# Esto es para produccion. Si va por gunicorn entonces el wsgi ejectura el settings de produccion
# python /app/manage.py collectstatic --noinput
# /usr/local/bin/gunicorn config.wsgi --bind 0.0.0.0:5000 --chdir=/app/backend

# Esto es para desarrollo
python /app/manage.py migrate
python /app/manage.py runserver 0.0.0.0:8000

