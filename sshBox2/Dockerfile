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
RUN useradd -ms /bin/bash ritlug2
RUN echo ritlug2:hidden003 | chpasswd

# adds our infinite run ssh server script
RUN mkdir -p /var/run/sshd
COPY bin/* /usr/local/bin/

# Copies the hint into the home director of user
COPY hint.md /home/ritlug2
RUN mkdir -p /home/ritlug2/.ssh/
RUN chown ritlug2:ritlug2 /home/ritlug2/.ssh
RUN touch /home/ritlug2/.ssh/authorized_keys
RUN chmod 700 /home/ritlug2/.ssh
RUN chmod 664 /home/ritlug2/.ssh/authorized_keys
COPY ssh/* /home/ritlug2/.ssh


RUN chmod 0555 /home/ritlug2/

# executes the ssh server at start
ENTRYPOINT ["ssh-start"]
CMD ["ssh-server"]
