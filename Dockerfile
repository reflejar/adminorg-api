# Stage 1
FROM python:3.7 as base

ENV PYTHONUNBUFFERED 1

ADD requirements /api/requirements

RUN apt-get update

RUN pip install -r /api/requirements/prod.txt

COPY ./bash/* /
RUN sed -i 's/\r//' /*.sh 
RUN chmod +x /*.sh

ADD api /api 
RUN chmod +x /api

RUN mkdir -p /api/media 
RUN chmod +x /api/media

ARG BUILD_DATE
ARG REVISION
ARG VERSION
LABEL maintainer "marianovaldez92@protonmail.com"
LABEL created $BUILD_DATE
LABEL url "https://admin-smart.com"
LABEL source "git@github.com:AdminSmartLab/as-django.git"
LABEL version $VERSION
LABEL revision $REVISION
LABEL vendor "AdminSmartLab"
LABEL title "AdminSmart Core API"
LABEL description "API for core of AdminSmart"

ENV PYTHONUNBUFFERED 1
WORKDIR /api
EXPOSE 8000
ENTRYPOINT ["/entrypoint.sh"]