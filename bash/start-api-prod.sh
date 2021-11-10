#!/bin/sh

set -o errexit
set -o pipefail
set -o nounset

export CELERY_BROKER_URL="${REDIS_URL}"
export DATABASE_URL="postgres://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${POSTGRES_HOST}:${POSTGRES_PORT}/${POSTGRES_DB}"

/usr/local/bin/gunicorn config.wsgi --bind 0.0.0.0:8000 --chdir=/api