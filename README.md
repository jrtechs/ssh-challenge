# Installation and Running on Debian VM

## Install Docker

```
apt update
apt upgrade
apt install apt-transport-https ca-certificates curl software-properties-common gnupg2
curl -fsSL https://download.docker.com/linux/debian/gpg | sudo apt-key add -
add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/debian $(lsb_release -cs) stable"

apt update
apt install docker-ce
```


## Install Docker-Compose

```
curl -L https://github.com/docker/compose/releases/download/1.25.0-rc2/docker-compose-`uname -s`-`uname -m` -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose
```


## Create Firewall

Create firewall to block everything that is not ports 80 or 22

```
apt-get install ufw
ufw enable
ufw allow 22:80/tcp
ufw deny 1000:9999/tcp
```

### Docker Firewall Trickery

Docker tampers directly with IPTables, so, ufw alone won't block people from accessing the internal services running on ports 7777, etc.

#### When When Running Single Container

Edit /etc/default/docker and uncomment the DOCKER_OPTS line:

```
DOCKER_OPTS="--dns 8.8.8.8 --dns 8.8.4.4 --iptables=false"
```

#### Running Docker Compose

Since we are using systemd with Docker Compose, we have to set the iptables flag by creating the following file with:

/etc/docker/daemon.json

```
{
    "iptables": false
}
```


## Add Base User For Demo

```
useradd -ms /bin/bash ritlug
echo ritlug:ritLugSep6! | chpasswd
```

## Install project files on system

```
git clone https://github.com/jrtechs/ssh-challenge.git

cd ssh-challenge

# Prevents the ritlug user from modifying the hint file
cp hint.md /home/ritlug/hint.md
chmod 0555 /home/ritlug/
```

# Running the Project

```
docker-compose build
docker-compose up
```
