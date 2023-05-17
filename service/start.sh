#!/bin/bash
python manage.py collectstatic --noinput&&
python manage.py makemigrations&&
python manage.py migrate&&
python manage.py import_china_area&&
uwsgi --ini /var/www/html/service/uwsgi_production.ini&&
tail -f /dev/null

exec "$@"