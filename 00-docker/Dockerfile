FROM ubuntu:20.04
MAINTAINER Tiago Antao <tiago@tiago.org>

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update; \
    apt-get upgrade -y; \
    apt-get install -y wget

RUN wget -O miniconda.sh http://repo.continuum.io/miniconda/Miniconda3-py38_4.9.2-Linux-x86_64.sh
# Presumes aceptance of the license
RUN bash miniconda.sh -b
ENV PATH="/root/miniconda3/bin:${PATH}"
RUN conda install \
    ipython==7.19.0 \
    line_profiler==2.1.2 \
    # psutil \
    # pympler \
    snakeviz==2.0.1 \
    zarr==2.6.1
RUN conda install -c bioconda plink

# docker build -t hpc .
# docker run -v /path_to_repo:/hpc -ti hpc /bin/bash
