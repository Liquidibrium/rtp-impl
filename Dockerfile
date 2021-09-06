FROM ubuntu:20.04

RUN apt update
RUN apt upgrade

# Install python 2.7
RUN apt install curl -y
RUN apt install python2.7 -y

# Install python2 pip
RUN curl https://bootstrap.pypa.io/pip/2.7/get-pip.py --output get-pip.py
RUN python2.7 get-pip.py

# Alias python to python2.7
RUN ln -s /usr/bin/python2.7 /usr/bin/python

WORKDIR /sandbox

CMD /bin/bash
# change "image-name"

# to build
# docker build -t image-name .

# run 
# docker run -it -v "$(pwd)":/sandbox image-name
# docker run -it -v %cd%:/sandbox hw3-rtp
# python2.7 TestHarness.py -s Sender.py -r Receiver.py