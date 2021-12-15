#!/bin/bash

rm -f './celerybeat.pid'
celery -A adminsmart.taskapp beat -l INFO
