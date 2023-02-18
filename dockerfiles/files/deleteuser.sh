#!/bin/sh
sudo deluser --remove-home $1
ps auxwww | grep sshd: | grep $1 | grep root | awk '{ print $1 }' | while read line; do pkill -s "$line"; done
