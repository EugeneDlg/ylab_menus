FROM python:3.10-slim

WORKDIR /celery

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY ./app/celery/requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt --no-cache-dir


COPY ./app/celery .

COPY .env .
