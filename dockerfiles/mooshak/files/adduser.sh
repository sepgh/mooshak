#!/bin/sh
sudo adduser -h /home/$1 -s /bin/sh -D $1
sudo echo -n "$1:$2" | chpasswd
