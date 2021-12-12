release: python manage.py flush --no-input
release: python manage.py makemigrations --noinput
release: python manage.py migrate --noinput
web: gunicorn AnimalsMarketplace.wsgi:application --log-file -