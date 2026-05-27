#!/bin/bash

export PGUSER="postgres"
export PGPASSWORD="123"
export PGHOST="localhost"
export PGPORT="5432"

echo "Запуск настройки БД..."

for db in main_db input_db stat_db; do
    psql -c "CREATE DATABASE ${db};" 2>/dev/null && echo "Создана база ${db}" 
done

for item in main_user:123 input_user:123 stat_user:123; do
    psql -c "CREATE USER ${item%%:*} WITH PASSWORD '${item#*:}';" && echo "Юзер ${item%%:*} создан" 
done

for user in main_user input_user stat_user; do
    psql -c "ALTER ROLE ${user} SET timezone TO 'UTC';" && echo "Установлена timezone для ${user}"
    done

for user in main_user input_user stat_user; do
    psql -c "ALTER ROLE ${user} SET default_transaction_isolation TO 'read committed';" && echo "Установлен read committed"
    done

for user in main_user input_user stat_user; do 
    psql -c "ALTER ROLE ${user} SET client_encoding TO 'utf8';" && echo "Установлен utf 8"
    done

for item in main_db:main_user input_db:input_user stat_db:stat_user; do
    db=${item%%:*}
    user=${item##*:}
    psql -c "GRANT ALL PRIVILEGES ON DATABASE ${db} TO ${user};" && echo "GRANT ALL PRIVILEGES ON DATABASE ${db} TO ${user}"
    psql -c "ALTER DATABASE $db OWNER TO $user;" && echo "ALTER DATABASE $db OWNER TO $user;"
    done



echo "Текущие базы:"
psql -c "SELECT datname FROM pg_database WHERE datname LIKE '%_db';"



