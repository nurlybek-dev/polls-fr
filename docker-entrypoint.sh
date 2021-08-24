cd src
python manage.py makemigrations
python manage.py migrate --noinput
python manage.py loaddata data.json
python manage.py runserver 0.0.0.0:8000