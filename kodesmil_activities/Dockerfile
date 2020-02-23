FROM python:3.9.0a1-alpine3.10

LABEL MAINTAINER="KodeSmil <hello@kodesmil.com>"

ENV GROUP_ID=1000 \
    USER_ID=1000

RUN apk add build-base
RUN apk add linux-headers

WORKDIR /var/www/

ADD . /var/www/
RUN pip install -r requirements.txt
RUN pip install gunicorn

RUN addgroup -g $GROUP_ID www
RUN adduser -D -u $USER_ID -G www www -s /bin/sh
RUN chown -R www /usr/local/lib/python3.9/site-packages

USER www

EXPOSE 5000

CMD [ "gunicorn", "-w", "4", "--bind", "0.0.0.0:5000", "app.wsgi"]