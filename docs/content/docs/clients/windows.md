---
title: "Windows Client"
type: docs
---

# Mooshak Windows Client

This page describess how to run Mooshak Windows Client.

This client is written in python for easier development in future. There is no pre-built executable ready at this moment. If you don't want to install python you can try [poormans vpn](https://github.com/sepgh/poormans-vpn) batch script.


## Requirements

To use Mooshak windows client, you will need to install python interpreter installed on your system(tested on 3.8, but 3.6+ is enough).


## Installation

First, clone the repository or download it as a zip and move it into directory of your choice. We assume this directory is called `mooshak`.

- Open CMD and navigate to `mooshak\clients\windows` directory.
- Start a new python virtual environment: `python -m venv venv`
- Activate the newly created virtual environment: `venv\Scripts\activate`
- Install requirements: `pip install -r requirements.txt`


## Configuration

Navigate to `mooshak\clients\windows` and create a new file named `client.json`.

Edit this file and replace the sample below with the values of your choice:

```json
{
  "socks_port": 8000,
  "server": "14.15.16.17",
  "username": "test",
  "password": "test",
  "port": 2255
}
```

The `socks_port` will be used on local machine to listen for incoming socks connections. `server` is ip address or hostname of the remote proxy server. `username` and `password` are SSH credentials. `port` is remote server port.

To use Websocket tunneling try below example:

```
{
  "socks_port": 8000,
  "ws": true,
  "ws_server": "wss://your_host",
  "ws_path_prefix": "mooshak",
  "ws_listen_port": 6000,
  "username": "test",
  "password": "test"
}
```

The value of `ws_path_prefix` should be the same one as in `Nginx` path configuration on server side, however this field is not mandatory.


## Running client

First run a new `Command Promot` **as administrator**.

Navigate to `mooshak\clients\windows` from CMD and activate the virtual environment using `venv\Scripts\activate`.

Then execute: `python mooshak.py` to get CLI access for Mooshak client. You can type in `start` to start the client, `stop` to stop it, and `help` to see all available commands.


{{< hint info >}}
You will need to keep the application open since there are no daemon services running as mooshak client on your system.
{{< /hint >}}

{{< hint warning >}}
Closing the `start`ed application without first executing `stop` command will result in your system forwarding connections to unexisting DNS and Tunnel! **Make sure to first execute `stop` command before leaving** and if you forgot, run the application again and then execute `stop` command to fix.
{{< /hint >}}
