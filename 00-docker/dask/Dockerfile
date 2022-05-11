FROM tiagoantao/python-performance
MAINTAINER Tiago Antao <tiago@tiago.org>

ENV DEBIAN_FRONTEND noninteractive

ENV PATH="/root/miniconda3/bin:${PATH}"
RUN conda install dask zarr cython
RUN pip install pyarrow
RUN pip install graphviz
