---
title: "Linux Client"
type: docs
---

# Mooshak Linux Client

Mooshak Linux Client uses [`sshuttle`](https://github.com/sshuttle/sshuttle) internally and it just handles what arguments are passed to `sshuttle` if ran with or without websocket tunnel.

## Requirements

To use Mooshak linux client, you will need to install python interpreter installed on your system(tested on 3.8, but 3.6+ is enough).


## Installation

First, clone the repository or download it as a zip and move it into directory of your choice. We assume this directory is called `mooshak`.

- Open terminal and navigate to `mooshak/clients/linux` directory.
- Start a new python virtual environment: `python -m venv venv`
- Activate the newly created virtual environment: `venv/bin/activate`
- Install requirements: `pip install -r requirements.txt`


## Configuration

Navigate to `mooshak/clients/linux` and create a new file named `client.json`.

Edit this file and replace the sample below with the values of your choice:

```json
{
  "server": "14.15.16.17",
  "username": "test",
  "port": 2255,
}
```

`server` is ip address or hostname of the remote ssh server. `username` is for ssh user and you will be prompted for the password. `port` is remote server port.

To use Websocket tunneling try below example:

```json
{
  "ws": true,
  "ws_server": "wss://your_host",
  "ws_path_prefix": "mooshak",
  "ws_listen_port": 6000,
  "username": "test",
}
```

The value of `ws_path_prefix` should be the same one as in `Nginx` path configuration on server side, however this field is not mandatory.


## Running client

Navigate to `mooshak/clients/linux` from terminal and activate the virtual environment using `venv/bin/activate`.

Then execute `python mooshak.py connect` to connect to the client and use `Control + C` to disconnect and exit.


{{< hint info >}}
You will need to keep the application open since there are no daemon services running as mooshak client on your system.
{{< /hint >}}

