release: python manage.py makemigrations --noinput
release: python manage.py migrate --noinput
web: echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin', 'admin@myproject.com', 'admin')" | python manage.py shell
web: gunicorn AnimalsMarketplace.wsgi:application --log-file -