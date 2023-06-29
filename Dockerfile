FROM python:3.10-alpine3.17
ENV TZ="Europe/Moscow"

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

EXPOSE 8000

WORKDIR /opt/online_shop

COPY . .

RUN apk add --update --no-cache --virtual .tmp-build-deps \
        gcc libc-dev linux-headers py3-pillow py3-cffi py3-brotli musl-dev pango && \
    pip install --upgrade pip && \
    pip install -r requirements/base.txt