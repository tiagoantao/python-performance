FROM ubuntu:22.04
MAINTAINER Tiago Antao <tiago@tiago.org>

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update; \
    apt-get upgrade -y; \
    apt-get install -y wget

RUN wget -O miniconda.sh https://repo.anaconda.com/miniconda/Miniconda3-py37_4.11.0-Linux-x86_64.sh
# Presumes aceptance of the license
RUN bash miniconda.sh -b
ENV PATH="/root/miniconda3/bin:${PATH}"
RUN conda install \
    python=3.10 \
    ipython=8.3
    
RUN conda install pandas=1.4 requests snakeviz line_profiler blosc
