# @author Jeffery Russell 9-1-19


# Base image
FROM ubuntu

# installs ssh server and nginx
RUN apt-get update \
    && apt-get install -y --no-install-recommends openssh-server \
    && apt-get install -y --no-install-recommends nginx \
    && apt-get clean

# adds user for ssh connection
RUN useradd -ms /bin/bash ritlug6
RUN echo ritlug6:finalPassword | chpasswd
RUN echo "PasswordAuthentication yes" >> /etc/ssh/sshd_config

RUN mkdir /var/run/sshd \
    && chmod 755 -R /var/run/sshd

# copies in the nginx config for the reverse proxy website
COPY nginx.conf /etc/nginx/nginx.conf

# runs ssh-server in background and nginx in foreground
CMD /usr/sbin/sshd & nginx -g "daemon off;"
