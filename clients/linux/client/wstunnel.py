import os
import subprocess

from termcolor import cprint


class WSTunnel:

    def __init__(self, server: str, ws_port: int = 8000, path_prefix=None):
        self.server = server
        self.ws_port = ws_port
        self.path_prefix = path_prefix
        self.subprocess = None

    def get_process_path(self):
        return os.path.join(
            os.path.relpath("assets"),
            "wstunnel"
        )

    def start(self):
        command: str = f"{self.get_process_path()} -L {self.ws_port}:mooshak:22 {self.server}"
        if self.path_prefix is not None:
            command += f" --upgradePathPrefix \"{self.path_prefix}\""
        self.subprocess = subprocess.Popen(
            command,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.STDOUT,
            shell=True,
        )
        cprint(f"Started WS connection to {self.server}", "yellow")

    def stop(self):
        if self.subprocess is not None:
            self.subprocess.terminate()
            self.subprocess.wait()
            self.subprocess = None

