FROM ubuntu:bionic

ENV PATH=/miniconda/bin:${PATH}

RUN apt-get -y update &&\
    apt-get -y install --no-install-recommends \
    procps openjdk-8-jdk curl &&\
    rm -rf /var/lib/apt/lists/*

ADD environment.yml /build/environment.yml

RUN cd /build && curl -LO http://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh &&\
    bash Miniconda3-latest-Linux-x86_64.sh -p /miniconda -b &&\
    conda env update --prefix /miniconda --file environment.yml  --prune  &&\
    cd / &&\
    rm -rf /build

ADD app.py /mzviewer/app.py
WORKDIR /mzviewer



