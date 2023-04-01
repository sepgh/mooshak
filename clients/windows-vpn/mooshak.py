import os
import signal
import sys
import time
from sys import exit

from termcolor import cprint

from client import rights, MooshakClient

os.system('color')

BANNER = """
   __  ___              __        __   \n
  /  |/  /__  ___  ___ / /  ___ _/ /__ \n
 / /|_/ / _ \/ _ \(_-</ _ \/ _ `/  '_/ \n
/_/  /_/\___/\___/___/_//_/\_,_/_/\_\  \n
VPN version
Version 1.0 - Developed by SepGh
Project URL: https://github.com/sepgh/mooshak
"""

if __name__ == '__main__':
    if not rights.is_user_admin():
        cprint("Run this program as administrator", "red")
        exit(0)

    if len(sys.argv) < 2:
        cprint("Argument missing. Choose between: connect, disconnect", "yellow")
        exit(0)

    command = sys.argv[1]

    # Connect
    if command == "connect":
        cprint(BANNER, "light_cyan")

        client = MooshakClient()

        def signal_handler(signal, frame):
            cprint('Disconnecting gracefully ...', 'yellow')
            client.stop()
            cprint('Disconnected', 'red')
            sys.exit(0)

        signal.signal(signal.SIGINT, signal_handler)
        client.start()

        cprint('Press Ctrl+C to disconnect')
        while True:
            try:
                time.sleep(3)
            except InterruptedError:
                signal.raise_signal(signal.SIGINT)

    elif command == "disconnect":
        MooshakClient().stop()

    else:
        cprint("Unknown command.")
        exit(0)
