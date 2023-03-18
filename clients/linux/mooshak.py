import signal
import sys
import time
from sys import exit

from termcolor import cprint

from client import MooshakClient
from client.assets_loader import validate_assets

BANNER = """
   __  ___              __        __   \n
  /  |/  /__  ___  ___ / /  ___ _/ /__ \n
 / /|_/ / _ \/ _ \(_-</ _ \/ _ `/  '_/ \n
/_/  /_/\___/\___/___/_//_/\_,_/_/\_\  \n
Version 1.0 - Developed by SepGh
Project URL: https://github.com/sepgh/mooshak
"""

if __name__ == '__main__':

    if len(sys.argv) < 2:
        print("Argument missing. Choose between: load_assets, connect")
        exit(0)

    command = sys.argv[1]

    # Connect
    if command == "connect":
        cprint(BANNER, "light_cyan")

        client = MooshakClient()

        def signal_handler(signal, frame):
            cprint('Disconnecting gracefully ...', 'green')
            client.stop()
            cprint('Disconnected', 'red')
            sys.exit(0)

        signal.signal(signal.SIGINT, signal_handler)
        client.start()
        signal.raise_signal(signal.SIGINT)

    elif command == "load_assets":
        validate_assets()

    else:
        MooshakClient().sshuttle_args()
        cprint("Unknown command.")
        exit(0)
