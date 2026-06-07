#!/bin/sh
echo Start
python manage.py makemigrations
python manage.py migrate
python manage.py loaddata diseases.json
python manage.py runserver 0.0.0.0:8000