#!/bin/sh

set -o errexit
set -o nounset


celery -A adminsmart.taskapp worker -l INFO
