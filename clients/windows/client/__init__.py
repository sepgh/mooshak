import json
import os.path

from termcolor import cprint

import client.assets_loader
import client.dns
import client.plink
from client.wstunnel import WSTunnel


def get_configuration() -> str:
    return os.path.join(
        os.path.relpath("."),
        "client.json"
    )


class MooshakClient:

    def __init__(self):
        with open(get_configuration(), "r") as configuration_file:
            self.configuration: dict = json.load(configuration_file)
        self.dns2socks = dns.DNS2Socks(
            self.configuration.get("socks_port", 6060),
            self.configuration.get("dns_server", "8.8.8.8"),
            self.configuration.get("dns_port", 53),
        )
        self.wstunnel = None
        if self.configuration.get("ws", False):
            cprint("Websocket configuration enabled.", "yellow")
            self.wstunnel = WSTunnel(
                self.configuration.get("ws_server"),
                self.configuration.get("ws_listen_port"),
                self.configuration.get("ws_path_prefix"),
            )
        self.plink = plink.PLink(
            self.configuration.get("socks_port", 6060),
            self.get_server(),
            self.get_server_port(),
            self.configuration.get("username", "unknown"),
            self.configuration.get("password", "unknown"),
            self.configuration.get("host_key", "unknown"),
        )

    def get_server(self):
        return self.configuration.get("server") if not self.configuration.get("ws", False) else "127.0.0.1"

    def get_server_port(self):
        return self.configuration.get(
            "port"
        ) if not self.configuration.get("ws", False) else self.configuration.get("ws_listen_port", 8000)

    def start(self):
        cprint("Starting Mooshak Client ...", "yellow")
        if self.wstunnel:
            self.wstunnel.start()
        self.plink.start()
        self.dns2socks.start()

    def stop(self):
        self.dns2socks.stop()
        self.plink.stop()
        if self.wstunnel:
            self.wstunnel.stop()
