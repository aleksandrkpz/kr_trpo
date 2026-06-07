#!/bin/bash
docker compose exec -T input python manage.py test && \
docker compose exec - T stat python manage.py test && \
docker compose exec -T main python manage.py test

