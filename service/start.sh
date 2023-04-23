#!/bin/bash
# while ! nc -z db 3306 ; do
#     echo "Waiting for the MySQL Server"
#     sleep 3
# done

python manage.py collectstatic --noinput&&
python manage.py makemigrations&&
python manage.py migrate&&
python manage.py import_china_area&&
uwsgi --ini /var/www/html/service/uwsgi_production.ini&&
tail -f /dev/null

exec "$@"