#!/bin/sh
# entrypoint.sh

# Chạy lệnh migrate
python manage.py migrate

# Khởi động Gunicorn
exec gunicorn --bind 0.0.0.0:8000 vsl.wsgi:application
        