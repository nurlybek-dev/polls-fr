FROM python:3-alpine

WORKDIR /code

COPY requirements.txt requirements.txt
RUN python -m pip install -r requirements.txt

COPY . .

CMD sh docker-entrypoint.sh
