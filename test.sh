#!bin/bash
docker compose exec input python manage.py test && \
docker compose exec stat python manage.py test && \
docker compose exec main python manage.py test

