import json
import os.path

from termcolor import cprint

import client.assets_loader
from client.ssh import SShuttleController
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
        self.wstunnel = None
        if self.configuration.get("ws", False):
            self.wstunnel = WSTunnel(
                self.configuration.get("ws_server"),
                self.configuration.get("ws_listen_port"),
                self.configuration.get("ws_path_prefix"),
            )
        self.sshuttle = SShuttleController(
            self.get_server(),
            self.get_server_port(),
            self.configuration.get("username", "unknown"),
        )

    def get_server(self):
        return self.configuration.get("server") if not self.configuration.get("ws", False) else "localhost"

    def get_server_port(self):
        return self.configuration.get(
            "port"
        ) if not self.configuration.get("ws", False) else self.configuration.get("ws_listen_port", 8000)

    def start(self):
        cprint("Starting Mooshak Client ...", "yellow")
        if self.wstunnel:
            cprint("Websocket configuration enabled.", "yellow")
            self.wstunnel.start()
        self.sshuttle.start()

    def sshuttle_args(self):
        self.sshuttle.sshuttle_args()
