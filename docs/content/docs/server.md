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

---



