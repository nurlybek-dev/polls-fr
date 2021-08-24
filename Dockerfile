FROM python:3-alpine

COPY . .

WORKDIR /code

RUN pip install pipenv && pipenv install

WORKDIR /src

RUN pipenv run python manage.py migrate --noinput
RUN pipenv run python manage.py loaddata data.json

CMD RUN pipenv run python manage.py runserver 0.0.0.0:8000
