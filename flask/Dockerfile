FROM python:3.9-alpine as base
FROM base as builder

EXPOSE 8002

# update apk repo
RUN echo "http://dl-4.alpinelinux.org/alpine/v3.14/main" >> /etc/apk/repositories && \
    echo "http://dl-4.alpinelinux.org/alpine/v3.14/community" >> /etc/apk/repositories

# install chromedriver
RUN apk update
RUN apk add chromium chromium-chromedriver

# install python add on
RUN apk add openssl-dev libffi-dev gcc musl-dev g++

# set display port to avoid crash
ENV DISPLAY=:99

# upgrade pip
RUN pip3 install --upgrade pip
RUN pip3 install pipenv

COPY Pipfile.lock /
COPY Pipfile /
RUN pipenv lock -r > requirements.txt
RUN pip install -r requirements.txt

COPY . /flask
WORKDIR /flask