# Stage 1
FROM python:3.7 as base

ENV PYTHONUNBUFFERED 1

ADD requirements /app/requirements

RUN apt-get update

RUN pip install -r /app/requirements/prod.txt

COPY ./bash/* /
RUN sed -i 's/\r//' /*.sh 
RUN chmod +x /*.sh

ADD app /app 
RUN chmod +x /app

RUN mkdir -p /app/adminsmart/media 
RUN chmod +x /app/adminsmart/media

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
WORKDIR /app
EXPOSE 8000
ENTRYPOINT ["/entrypoint.sh"]