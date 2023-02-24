import json
import os.path

from termcolor import cprint

import client.assets_loader
import client.dns
import client.plink


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
        self.plink = plink.PLink(
            self.configuration.get("socks_port", 6060),
            self.get_server(),
            self.get_server_port(),
            self.configuration.get("username", "unknown"),
            self.configuration.get("password", "unknown"),
            lambda: self.stop()
        )

    def get_server(self):
        return self.configuration.get("server") if not self.configuration.get("ws", False) else "127.0.0.1"

    def get_server_port(self):
        return self.configuration.get("port") if not self.configuration.get("ws", False) else 2255

    def start(self):
        cprint("Starting Mooshak Client ...", "yellow")
        self.dns2socks.start()
        self.plink.start()

    def stop(self):
        self.dns2socks.stop()
        self.plink.stop()
