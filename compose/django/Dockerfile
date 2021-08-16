FROM python:3.7-alpine3.13

ENV PYTHONUNBUFFERED 1

ADD django/requirements/prod.txt /app/requirements.txt

RUN set -ex \
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
  && apk add build-base libressl-dev libffi-dev cargo openssl-dev \

  && /env/bin/pip install --upgrade pip \
  && /env/bin/pip install Cython cffi paramiko \
  && /env/bin/pip install -r /app/requirements.txt \

COPY ./compose/django/entrypoint.sh /entrypoint.sh
RUN sed -i 's/\r//' /entrypoint.sh

COPY ./compose/django/celery/worker/start /start-celeryworker.sh
RUN sed -i 's/\r//' /start-celeryworker.sh

COPY ./compose/django/celery/beat/start.sh /start-celerybeat.sh
RUN sed -i 's/\r//' /start-celerybeat.sh

COPY ./compose/django/celery/flower/start.sh /start-flower.sh
RUN sed -i 's/\r//' /start-flower.sh

ADD django /app
WORKDIR /app

ENV VIRTUAL_ENV /env
ENV PATH /env/bin:$PATH

EXPOSE 8000

ENTRYPOINT ["/entrypoint.sh"]

CMD ["gunicorn", "--bind", ":8000", "--workers", "3", "config.wsgi" ]

