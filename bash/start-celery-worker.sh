#!/bin/bash

celery -A adminsmart.taskapp worker -l INFO
