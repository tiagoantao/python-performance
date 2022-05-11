FROM tiagoantao/python-performance
MAINTAINER Tiago Antao <tiago@tiago.org>

ENV DEBIAN_FRONTEND noninteractive

ENV PATH="/root/miniconda3/bin:${PATH}"
    
RUN apt install -y nvidia-compute-utils-510-server
RUN conda install -c rapidsai -c nvidia -c conda-forge cupy cudatoolkit numba
