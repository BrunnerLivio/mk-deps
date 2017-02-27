FROM ubuntu:latest
MAINTAINER "livio.brunner.lb1@gmail.com"

RUN apt-get update
RUN apt-get install -y  --no-install-recommends python3-debian python3-apt python3 dh-make build-essential devscripts python3-argcomplete python3-all python3-setuptools python3-pytest fakeroot

RUN mkdir -p /mk-deps
COPY . /mk-deps
WORKDIR /mk-deps 
