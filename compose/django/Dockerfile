FROM python:3.7-alpine3.13

ENV PYTHONUNBUFFERED 1

ADD django/requirements /app/requirements

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


RUN addgroup -S django \
    && adduser -S -G django django

RUN pip install Cython cffi paramiko
RUN pip install -r /app/requirements/prod.txt


COPY ./compose/django/entrypoint.sh /entrypoint.sh
RUN sed -i 's/\r//' /entrypoint.sh
RUN chmod +x /entrypoint.sh
RUN chown django /entrypoint.sh

COPY ./compose/django/start.sh /start.sh
RUN sed -i 's/\r//' /start.sh
RUN chmod +x /start.sh
RUN chown django /start.sh

ADD django /app
RUN chown -R django /app
USER django
WORKDIR /app

EXPOSE 8000

ENTRYPOINT ["/entrypoint.sh"]

#CMD ["gunicorn", "--bind", ":8000", "--workers", "3", "config.wsgi" ] # Para produccion. Esto ejecuta 3 workes de gunicorn para django y django ejecuta settings.produccion
CMD ["/start.sh"]

