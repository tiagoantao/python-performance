FROM ubuntu:eoan
MAINTAINER Tiago Antao <tiago@tiago.org>

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update; \
    apt-get upgrade -y; \
    apt-get install -y wget

RUN wget -O miniconda.sh http://repo.continuum.io/miniconda/Miniconda3-4.7.12.1-Linux-x86_64.sh
#Presumes aceptance of the license
RUN bash miniconda.sh -b

