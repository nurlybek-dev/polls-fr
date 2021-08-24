FROM python:3-alpine

COPY . /code/.

WORKDIR /code

RUN pip install pipenv && pipenv install

WORKDIR /code/src

RUN pipenv run python manage.py migrate --noinput
RUN pipenv run python manage.py loaddata data.json

CMD pipenv run python manage.py runserver 0.0.0.0:8000
