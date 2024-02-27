# Stage 1
FROM python:3.7 as base

ENV PYTHONUNBUFFERED 1

RUN apt-get update

ADD requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt

COPY ./entrypoint.sh /
RUN sed -i 's/\r//' /*.sh 
RUN chmod +x /*.sh

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
LABEL title "AdminOrg Insight Edition"

WORKDIR /app
EXPOSE 8000
ENTRYPOINT ["/entrypoint.sh"]
CMD [ "gunicorn", "config.wsgi", "--bind", "0.0.0.0:8000", "--chdir=/app", "--timeout", "1800" ]