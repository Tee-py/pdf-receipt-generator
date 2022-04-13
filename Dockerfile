FROM python:3.9.12-alpine

WORKDIR /app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DEBUG FALSE


# install psycopg2
RUN apk update \
    && apk add --virtual dukka zlib-dev jpeg-dev gcc musl-dev \
    && apk add postgresql-dev \
    && apk add libffi-dev \
    && apk add py3-pip py3-pillow py3-cffi gcc py3-brotli pango \
    && pip install psycopg2

# install dependencies
COPY ./requirements.txt .
# Upgrade pip
RUN pip install --upgrade pip==22.0.4
RUN pip install -r requirements.txt

# copy project
COPY . .

# collect static files
RUN python manage.py collectstatic --noinput

