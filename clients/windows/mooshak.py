import sys
import os
from nubia import Nubia, Options
from termcolor import cprint
from client import rights
import client.commands

os.system('color')

BANNER = """
   __  ___              __        __   \n
  /  |/  /__  ___  ___ / /  ___ _/ /__ \n
 / /|_/ / _ \/ _ \(_-</ _ \/ _ `/  '_/ \n
/_/  /_/\___/\___/___/_//_/\_,_/_/\_\  \n
Version 1.0 - Developed by SepGh
Project URL: https://github.com/sepgh/mooshak
"""

if __name__ == '__main__':
    if not rights.is_user_admin():
        cprint("Run this program as administrator", "red")
        exit(0)

    cprint(BANNER, "light_cyan")

    shell = Nubia(
        name="Mooshak Proxy CLI",
        command_pkgs=client,
        options=Options(persistent_history=False, auto_execute_single_suggestions=False),
    )
    sys.exit(shell.run())

