# Simple Docker file which runs a ssh
# server to connect to. A generic
# user is generated with a hard-coded
# password.
# 
# @author Jeffery Russell 8-26-19

# Basic Ubuntu Image
FROM ubuntu

ENV TERM xterm

# Installs openssh-server
RUN apt-get update && apt-get install -y --no-install-recommends \
    openssh-server \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

# Adds a dummy user to ssh into
RUN useradd -ms /bin/bash ritlug1
RUN echo ritlug1:password | chpasswd

# adds our infinite run ssh server script
RUN mkdir -p /var/run/sshd
COPY bin/* /usr/local/bin/

# Copies the hint into the home director of user
COPY hint.md /home/ritlug1

EXPOSE 8888

# executes the ssh server at start
ENTRYPOINT ["ssh-start"]
CMD ["ssh-server"]
