#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

python manage.py migrate

echo "Start tests..."
python -W ignore manage.py test

echo "Rebuild index..."
python manage.py search_index --rebuild -f


exec "$@"