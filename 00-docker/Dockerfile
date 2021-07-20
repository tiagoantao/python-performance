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
    python=3.9.5 \
    dask=2021.4.0 \
        ipython=7.22
RUN pip install python-graphviz
RUN conda install -c bioconda plink


# 
# apt install nvidia-utils-460-server
# conda install -c rapidsai -c nvidia -c numba -c conda-forge cudf cupy cudatoolkit=11.2
# docker build -t hpc .
# docker run -v /path_to_repo:/hpc -ti hpc /bin/bash
