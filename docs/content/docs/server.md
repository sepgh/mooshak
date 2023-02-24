---
title: "Server"
type: docs
---

# Mooshak Server


## Setup

To setup a mooshak server you will need `git`, `docker` and `docker compose` installed.


Go to directory of your choice and clone the project.

```bash
$ git clone https://github.com/sepgh/mooshak
```

Next, go to newly cloned `mooshak` directory and then navigate to `server` directory. After that you can start `mooshak` by runing the docker compose:

```bash
$ cd mooshak  # cloned directory
$ cd server  # server scripts
$ docker compose up -d  # or: docker-compose up -d
```

Congradulations! You have mooshak ready to be used. The SSH server will be available on port `2255`, and websocket tunnel will be available on port `3344`.

To stop the mooshak server go to the same directory and then use:

```bash
$ docker compose down
```

## Managing users

The `mooshak` container has scripts installed to help you add or remove users.

First you need to find the running container:

```shell
$ docker ps
```

Example output:

```
CONTAINER ID   IMAGE                COMMAND                  CREATED         STATUS         PORTS                                   NAMES
a8b04854bb35   mooshak10-wstunnel   "/bin/sh -c '/wstunn…"   4 seconds ago   Up 2 seconds   0.0.0.0:3344->80/tcp, :::3344->80/tcp   mooshak10-wstunnel-1
f1ac70f5d9bb   mooshak10-mooshak    "/entrypoint.sh"         4 seconds ago   Up 2 seconds   0.0.0.0:2255->22/tcp, :::2255->22/tcp   mooshak10-mooshak-1  # <--
```

The container ID we are looking for is `f1ac70f5d9bb` in this example, with image `mooshak{tag}-mooshak`.

To add a new user (or update their password) use:

```shell
$ docker exec <COONTAINER ID HERE> /adduser.sh <username> <password>

# Eaxmple valid output:  chpasswd: password for 'test' changed
```

To remove a user (and terminate their open session) use:

```shell
$ docker exec <COONTAINER ID HERE> /deleteuser.sh <username>

# Example valid output: deluser: can't find test in /etc/group
```



## Run behind Nginx - Websocket

You can configure your Nginx setup to forward websocket connections to websocket port listened by Mooshak WsTunnel (`3344`).

Here is a sample path configuration to add to your Nginx setup:

```
location /mooshak {
        proxy_pass http://127.0.0.1:3344;
        proxy_http_version  1.1;
        proxy_set_header    Upgrade $http_upgrade;
        proxy_set_header    Connection "upgrade";
        proxy_set_header    Host $http_host;
        proxy_set_header    X-Real-IP $remote_addr;

        proxy_connect_timeout       10m;
        proxy_send_timeout          10m;
        proxy_read_timeout          90m;
        send_timeout                10m;
}
```

Reload your Nginx service and you are good to go.
