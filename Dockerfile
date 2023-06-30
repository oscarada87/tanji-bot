FROM python:3.9-alpine

# update apk repo
RUN echo "http://dl-4.alpinelinux.org/alpine/v3.14/main" >> /etc/apk/repositories && \
    echo "http://dl-4.alpinelinux.org/alpine/v3.14/community" >> /etc/apk/repositories

# install chromedriver
RUN apk update && apk add chromium chromium-chromedriver

# set display port to avoid crash
ENV DISPLAY=:99

# upgrade pip
RUN pip3 install --upgrade pip

COPY requirements.txt /
RUN pip install -r requirements.txt

COPY . /src
WORKDIR /src