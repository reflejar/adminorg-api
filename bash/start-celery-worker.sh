#!/bin/bash

celery -A taskapp worker -l INFO --concurrency=2
