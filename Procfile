release: python manage.py makemigration --noinput
release: python manage.py migrate --noinput
web: gunicorn AnimalsMarketplace.wsgi:application --log-file -