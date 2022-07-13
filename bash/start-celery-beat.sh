#!/bin/bash

rm -f './celerybeat.pid'
celery -A taskapp beat -l INFO
