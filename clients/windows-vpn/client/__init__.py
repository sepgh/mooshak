import json
import signal

from termcolor import cprint

import client.plink
from client.configuration import get_configuration
from client.tester import SocksTester
from client.wstunnel import WSTunnel


class MooshakClient:

    def __init__(self):
        with open(get_configuration(), "r") as configuration_file:
            self.configuration: dict = json.load(configuration_file)

        self.wstunnel = None
        if self.configuration.get("ws", False):
            cprint("Websocket configuration enabled.", "yellow")
            self.wstunnel = WSTunnel(
                self.configuration.get("ws_server"),
                self.configuration.get("ws_listen_port"),
                self.configuration.get("ws_path_prefix"),
                self.configuration.get("verbose", False),
            )
        self.plink = plink.PLink(
            self.configuration.get("socks_port", 6060),
            self.get_server(),
            self.get_server_port(),
            self.configuration.get("username", "unknown"),
            self.configuration.get("password", "unknown"),
            self.configuration.get("host_key", "unknown"),
            self.configuration.get("verbose", False),
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
        if SocksTester(self.configuration).test() is False:
            self.stop()
            signal.raise_signal(signal.SIGINT)
        else:
            cprint("Connected", "green")

    def stop(self):
        self.plink.stop()
        if self.wstunnel:
            self.wstunnel.stop()
