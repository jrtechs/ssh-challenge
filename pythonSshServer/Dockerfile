# Docker script to run the custom python ssh-server
# which has a rit-lug trivia game on it.
#
# The most notable thing about this package 
# is the dependencies required to get the paramiko 
# python library working.

# @author Jeffyer Russell 8-27-19

FROM ubuntu

# Installs python and the dev libraries needed for paramiko
RUN apt-get update && apt-get install -y --no-install-recommends \
    python2.7 \
    && apt-get install -y python-dev \
    && apt-get install -y python-pip \
    && apt-get install -y libkrb5-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# adds custom ssh server python code
ADD ssh_server.py /
ADD test_rsa.key /

# installs pip dependencies
RUN pip install paramiko \
    && pip install python-gssapi

# runs the python script
CMD ["python", "./ssh_server.py"]
