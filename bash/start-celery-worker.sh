#!/bin/bash

celery -A adminsmart.taskapp worker -l INFO --concurrency=2
