FROM python:3.9

RUN apt-get update && apt-get install -y python3-pip
RUN pip3 install kafka-python

RUN mkdir /workdir
WORKDIR /workdir