#!/bin/bash

celery flower \
    --app=adminsmart.taskapp \
    --broker="${REDIS_URL}" \
    --basic_auth="${CELERY_FLOWER_USER}:${CELERY_FLOWER_PASSWORD}"
