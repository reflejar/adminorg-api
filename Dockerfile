# Stage 1
FROM python:3.7 as base

ENV PYTHONUNBUFFERED=1

RUN apt-get update && \
    apt-get install -y netcat-openbsd

ADD requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt

ADD wait-for-mysql.sh /wait-for-mysql.sh
RUN chmod +x /wait-for-mysql.sh

ADD app /app 
RUN chmod +x /app

RUN mkdir -p /app/media 
RUN chmod +x /app/media

ARG BUILD_DATE
ARG REVISION
ARG VERSION
LABEL maintainer "marianovaldez92@protonmail.com"
LABEL created $BUILD_DATE
LABEL version $VERSION
LABEL revision $REVISION
LABEL title "AdminOrg - API"

WORKDIR /app

RUN python manage.py collectstatic --noinput --clear

EXPOSE 8000
ENTRYPOINT ["/wait-for-mysql.sh"]
CMD set -xe; python manage.py migrate --noinput; gunicorn config.wsgi --bind 0.0.0.0:8000