#!/bin/bash
cd /app/
echo "Migrate Search Models"
python manage.py migrate
echo "Start Search Application on $AUDA_BACKEND_HOST:$AUDA_BACKEND_PORT"
gunicorn --bind $AUDA_BACKEND_HOST:$AUDA_BACKEND_PORT --workers $AUDA_BACKEND_WORKERS --access-logfile - --error-logfile - --log-level info auda.wsgi:application