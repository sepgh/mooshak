import os
import subprocess
import sys

from termcolor import cprint

from client.utils import VerbosePrinter


class WSTunnel:

    def __init__(self, server: str, ws_port: int = 8000, path_prefix=None, verbose:bool = False):
        self.server = server
        self.ws_port = ws_port
        self.path_prefix = path_prefix
        self.subprocess = None
        self.verbose = verbose
        self.verbose_printer: VerbosePrinter = None

    def get_process_path(self):
        return os.path.join(
            os.path.relpath("assets"),
            "wstunnel"
        )

    def start(self):
        command: str = f"{self.get_process_path()} -L {self.ws_port}:mooshak:22 {self.server}"
        if self.path_prefix is not None:
            command += f" --upgradePathPrefix \"{self.path_prefix}\""
        si = subprocess.STARTUPINFO()
        si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        if self.verbose:
            command += " -v"
        self.subprocess = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE if self.verbose else sys.stdout,
        )
        if self.verbose:
            self.verbose_printer = VerbosePrinter(self.subprocess, "wstunnel")
            self.verbose_printer.start()
        cprint(f"Started WS connection to {self.server}", "yellow")

    def stop(self):
        if self.subprocess is not None:
            self.subprocess.terminate()
            self.subprocess.wait()
            self.subprocess = None
        if self.verbose_printer is not None:
            self.verbose_printer.stop()
