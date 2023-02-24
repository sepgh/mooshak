```
  __  __                 _           _    
 |  \/  |               | |         | |   
 | \  / | ___   ___  ___| |__   __ _| | __
 | |\/| |/ _ \ / _ \/ __| '_ \ / _` | |/ /
 | |  | | (_) | (_) \__ \ | | | (_| |   < 
 |_|  |_|\___/ \___/|___/_| |_|\__,_|_|\_\
                                                                                    
Version 1.0
```

The purpose of this repository is to provide tools to setup `lightweight` and `easy-to-configure` proxy/tunneling service. This can help masking your identity on the internet and avoid internet cencorship.

**Mooshak :rocket:** (Farsi for Rocket/Shuttle) provides easy to setup dockerized SSH server, as well as support for [websocket](https://github.com/erebe/wstunnel) tunneling to turn SSH TCP connection look like legitimate HTTP(S) TCP connection.

Mooshak project also provides information (and source codes) for clients to be used for these connections.

---
### Documentation

Full documentation is available under https://sepgh.github.io/mooshak/

### Todo

- [X] SSH Server
- [x] WS Tunnel
- [X] Windows client
- [X] Server setup documentation
- [X] UDP Support (only on linux for now)
- [ ] Restricted shell for ssh clients
- [ ] Linux client
- [ ] MacOs client
- [ ] Android clients
- [ ] Limit python access on the server for `sshuttle`
