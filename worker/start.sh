#!/bin/bash

celery -A worker.celery worker --loglevel=info -E &
celery -A worker.celery beat --loglevel=info