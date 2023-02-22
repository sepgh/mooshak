import json
import sys
import assets_loader
import dns


def get_configuration() -> str:
    if len(sys.argv) > 1:
        return sys.argv[1]
    else:
        return "client.json"


class MooshakClient:

    def __init__(self):
        with open(get_configuration(), "r") as configuration_file:
            self.configuration: dict = json.load(configuration_file)
        assets_loader.validate_assets()
        self.dns2socks = dns.DNS2Socks(
            self.configuration.get("socks_port", 6060),
            self.configuration.get("dns_server", "8.8.8.8"),
            self.configuration.get("dns_port", 53),
        )

    def start(self):
        self.dns2socks.start()

    def stop(self):
        self.dns2socks.stop()
