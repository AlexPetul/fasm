FROM python:3.11-alpine

COPY ./Pipfile .
COPY ./Pipfile.lock .

RUN \
    apk update \
    && apk add --no-cache --virtual .build-deps-pkg postgresql-dev xvfb dbus build-base libffi-dev python3-dev musl-dev zlib-dev \
    && pip install --upgrade pip setuptools-scm pipenv \
    && pipenv install --system --ignore-pipfile --dev \
    && apk del --no-network --purge .build-deps-pkg \
    && rm -rf /root/.cache \
    && apk add --no-cache postgresql-libs libffi zlib libjpeg bash

COPY . /app

WORKDIR /app

EXPOSE 8000

CMD uvicorn src.main:app --reload --host 0.0.0.0 --port 8000