FROM python:3.9.0a1-alpine3.10

LABEL MAINTAINER="KodeSmil <hello@kodesmil.com>"

RUN pip install --upgrade pip
RUN pip install gunicorn

RUN adduser -D python
USER python
WORKDIR /home/python

ARG DEBUG=0
ENV FLASK_DEBUG $DEBUG

CMD [ "gunicorn", "-w", "1", "--bind", "0.0.0.0:5000", "src.wsgi", "--reload", "--timeout", "360"]

COPY --chown=python:python requirements.txt .
ENV PATH="/home/python/.local/bin:${PATH}"
RUN pip install --user -r requirements.txt

COPY --chown=python:python src src