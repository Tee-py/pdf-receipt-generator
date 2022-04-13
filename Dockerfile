FROM python:3.9.12-alpine

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DEBUG FALSE
ENV CLOUD_NAME teepy
ENV CLOUD_API_KEY 669776671592722
ENV CLOUD_API_SECRET oxfJWS9xIkA2wG6FFmFCb_zOCJI

RUN apk update \
    && apk add --virtual dukka zlib-dev jpeg-dev gcc musl-dev \
    && apk add postgresql-dev \
    && apk add libffi-dev \
    && apk add py3-pip py3-pillow py3-cffi gcc py3-brotli pango \
    && apk add fontconfig font-noto terminus-font \
    && pip install psycopg2

COPY ./requirements.txt .

RUN pip install --upgrade pip==22.0.4
RUN pip install -r requirements.txt

COPY . .

RUN python manage.py collectstatic --noinput



