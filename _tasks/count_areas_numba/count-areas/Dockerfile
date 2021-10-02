FROM python:3.7.7

RUN pip3 install numpy
RUN pip3 install numba

ENV PATH="/count-areas:${PATH}"
ADD . /count-areas
WORKDIR /count-areas
