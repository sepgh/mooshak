---
title: "Windows Client"
type: docs
---

# Mooshak Windows Client

This page describess how to run Mooshak Windows Client.

This client is written in python for easier development in future. If you don't want to install python you can try [pre-built version from releases](https://github.com/sepgh/mooshak/releases/tag/v1.0.0) or [poormans vpn](https://github.com/sepgh/poormans-vpn) batch script.


## How it works:

Mooshak Windows Client uses Putty Plink software to create a SSH Tunnel to the server. Additionally, Websocket Tunnel may be used on top of SSH Tunnel. Afterwards, the DNS2SOCKS will be used to redirect DNS traffic through SSH Tunnel, and windows proxy and DNS configuration will be changed. Mooshak itself hasn't implemented any of these tools and they are third party solutions that are gathered together in the client.


## Requirements (from source)

To use Mooshak windows client from source, you will need to install python interpreter installed on your system(tested on 3.8, but 3.6+ is enough).


## Installation (from source)

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
  "port": 2255,
  "host_key": "SHA256:aSB62hUG4e0IuMffB/bxiaA+hxQMK5asdalaZk/EQ+A",
  "verbose": false
}
```

The `socks_port` will be used on local machine to listen for incoming socks connections. `server` is ip address or hostname of the remote proxy server. `username` and `password` are SSH credentials. `port` is remote server port.

To debug the connection you can set `verbose` to `true` to get log of Plink and WsTunnel.

To use Websocket tunneling try below example:

```json
{
  "socks_port": 8000,
  "ws": true,
  "ws_server": "wss://your_host",
  "ws_path_prefix": "mooshak",
  "ws_listen_port": 6000,
  "username": "test",
  "password": "test",
  "host_key": "SHA256:aSB62hUG4e0IuMffB/bxiaA+hxQMK5asdalaZk/EQ+A"
}
```

The value of `ws_path_prefix` should be the same one as in `Nginx` path configuration on server side, however this field is not mandatory.

{{< hint info >}}
If you are using pre-built version then keep this configuration file right next to the executable file.
{{< /hint >}}

## Running client

### From source
First run a new `Command Promot` **as administrator**.

Navigate to `mooshak\clients\windows` from CMD and activate the virtual environment using `venv\Scripts\activate`.

Then execute: `python mooshak.py connect` to connect and disconnect with `Control + C`. If you close the window withoug `Control + C` it wont disconnect completely and you will need to do `mooshak.exe disconnect`.

### From pre-built

First run a new `Command Promot` **as administrator** and navigate to where your executable file is.

Then execute `mooshak.exe connect` to connect and disconnect with `Control + C`. If you close the window withoug `Control + C` it wont disconnect completely and you will need to do `mooshak.exe disconnect`.

**Important:** If you are running pre-built you will need to either create a folder called `assets` next to your executable file and then download all of the assets from [this link](https://github.com/sepgh/mooshak/tree/main/clients/windows/assets) there, or you can run `mooshak.exe load_assets` so it will download external dependencies for you automatically.

---

{{< hint info >}}
You will need to keep the application open since there are no daemon services running as mooshak client on your system. (for both pre-built and python)
{{< /hint >}}
