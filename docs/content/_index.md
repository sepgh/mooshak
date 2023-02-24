---
title: "Home"
type: docs
bookToc: false
---

![Logo](/static/logo.png)

## Introduction

**Mooshak** (Farsi for Rocket/Shuttle) provides easy to setup dockerized SSH server, as well as support for [websocket](https://github.com/erebe/wstunnel) tunneling to turn SSH TCP connection look like legitimate HTTP(S) TCP connection.

The purpose of this project is to provide tools to setup `lightweight` and `easy-to-configure` proxy/tunneling service. This can help masking your identity on the internet and avoid internet cencorship.

{{< hint warning >}} 
I strongly recommend you not to provide Mooshak server as a paid/free service open to "untrusted" users. The server will run in docker containers to add one level of security from people whom access your SSH Tunnel, however that is not enough.

Any personal use should be safe, and maybe you can share it with people you trust as well.


Unfortunately, due to `sshuttle` requirements, it's not easy to set `restricted bash` for users, and they will all have access to `python` command. Feel free to contribute to the project if you have suggesions on making Mooshak server more secure while keeping it simple.
{{< /hint >}}

