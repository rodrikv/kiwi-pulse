#! /bin/bash
python manage.py makemigrations
python manage.py migrate

python manage.py collectstatic --noinput --skip-checks

echo "from django.contrib.auth.models import User;User.objects.all().delete(); User.objects.create_superuser('admin', 'example@google.com', 'admin')" | python manage.py shell
gunicorn instager.wsgi:application -b 0.0.0.0:8000