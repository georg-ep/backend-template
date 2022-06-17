FROM python:3.9
LABEL MAINTAINER="GoShopTheMarket.co"
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get -y dist-upgrade
RUN apt install -y netcat

COPY ./requirements.txt /requirements.txt
RUN pip3 install --upgrade pip
RUN pip3 install -r /requirements.txt


RUN mkdir /app
WORKDIR /app
COPY entrypoint.sh /entrypoint.sh
COPY ./app /app

RUN mkdir /tmp/runtime-user

ENTRYPOINT ["/entrypoint.sh"]
