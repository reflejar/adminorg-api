#!/bin/bash

/usr/local/bin/gunicorn config.wsgi --bind 0.0.0.0:8000 --chdir=/api --timeout 360