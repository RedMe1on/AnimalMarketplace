release: python manage.py makemigrations
release: python manage.py migrate --noinput
web: gunicorn AnimalsMarketplace.wsgi:application --log-file -