# Stage 1
FROM python:3.7-alpine3.13 as base

ADD requirements /api/requirements

RUN apk update \
  # psycopg2 dependencies
  && apk add --virtual build-deps gcc python3-dev musl-dev \
  && apk add postgresql-dev postgresql-client \
  # Pillow dependencies
  && apk add jpeg-dev zlib-dev freetype-dev lcms2-dev openjpeg-dev tiff-dev tk-dev tcl-dev \
  # CFFI dependencies
  && apk add libffi-dev py-cffi \
  # Translations dependencies
  && apk add gettext \
  # AdminSmart dependencies
  && apk add libxml2-dev libxslt-dev py3-lxml cairo-dev pango-dev gdk-pixbuf-dev g++ \
  # Fonts
  && apk add ttf-opensans \
  # OpenSSL
  && apk add build-base libressl-dev libffi-dev cargo openssl-dev

RUN pip install -r /api/requirements/prod.txt

COPY ./bash/* /
RUN sed -i 's/\r//' /*.sh 
RUN chmod +x /*.sh

ADD api /api 
RUN chmod +x /api

RUN mkdir -p /api/media 
RUN chmod +x /api/media



# Stage 2
FROM python:3.7-alpine3.13

ENV PYTHONUNBUFFERED 1

WORKDIR /api
COPY --from=base /usr/local/lib/python3.7/site-packages/ /usr/local/lib/python3.7/site-packages/
COPY --from=base /usr/local/bin/ /usr/local/bin/
COPY --from=base /usr/lib/*.so* /usr/lib/
COPY --from=base /lib /lib
COPY --from=base /api /api
COPY --from=base /*.sh /


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

EXPOSE 8000
ENTRYPOINT ["/entrypoint.sh"]