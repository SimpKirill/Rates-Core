#!/bin/bash

celery -A core.celery worker --loglevel=info -E &
celery -A core.celery beat --loglevel=info