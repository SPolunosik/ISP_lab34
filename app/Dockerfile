
# syntax=docker/dockerfile:1
FROM python:3
ENV PYTHONUNBUFFERED=1
WORKDIR /code
COPY pip-requirements.txt requirements.txt
RUN set -ex; \
    pip install -r requirements.txt \
    && rm requirements.txt
EXPOSE 8000
COPY . .
