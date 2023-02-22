import json
import signal
import sys
import threading

import assets


def get_configuration() -> str:
    if len(sys.argv) > 1:
        return sys.argv[1]
    else:
        return "client.json"


class MooshakClient:

    def __init__(self):
        with open(get_configuration(), "r") as configuration_file:
            self.configuration = json.load(configuration_file)
        assets.validate_assets()

    def start(self):
        print("started")

    def stop(self):
        print("Bye")


MOOSHAK_CLIENT = MooshakClient()


def signal_handler(signal, frame):
    print('Shutting down gracefully ...')
    MOOSHAK_CLIENT.stop()
    sys.exit(0)


if __name__ == '__main__':
    MOOSHAK_CLIENT.start()

    signal.signal(signal.SIGINT, signal_handler)
    print('Press Ctrl+C')
    forever = threading.Event()
    forever.wait()

