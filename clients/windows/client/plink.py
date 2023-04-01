import os
import subprocess
import sys

from termcolor import cprint

from client.utils import VerbosePrinter
from client.win import setup_windows_proxy, drop_windows_proxy


class PLink:

    def __init__(
            self,
            socks_port: int,
            server: str,
            server_port: int,
            username: str,
            password: str,
            host_key: str,
            verbose: bool = False
    ):
        self.socks_port = socks_port
        self.server = server
        self.server_port = server_port
        self.username = username
        self.password = password
        self.host_key = host_key
        self.process_thread = None
        self.subprocess = None
        self.stopped = False
        self.verbose = verbose
        self.verbose_printer: VerbosePrinter = None

    def get_process_path(self):
        return os.path.join(
            os.path.relpath("assets"),
            "plink.exe"
        )

    def _get_command(self):
        command = f"{self.get_process_path()} -hostkey {self.host_key} -ssh {self.server} -D {self.socks_port}  -l {self.username} -P {self.server_port} -no-antispoof -pw {self.password} "
        if self.verbose:
            command += "-v -sanitise-stderr -sanitise-stderr"
        return command

    def start(self):
        if self.process_thread is not None:
            return

        self.subprocess = subprocess.Popen(
            self._get_command(),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        if self.verbose:
            self.verbose_printer = VerbosePrinter(self.subprocess, "plink", out=False)
            self.verbose_printer.start()
        cprint(f"Ran Plink to create SSH Tunnel (socks) on port {self.socks_port}", 'yellow')
        self.stopped = False
        setup_windows_proxy(self.socks_port)

    def stop(self):
        current_stop_status = self.stopped
        if self.subprocess is not None:
            self.stopped = True
            self.subprocess.terminate()
            self.subprocess.wait()
            self.subprocess = None
        if not current_stop_status:
            drop_windows_proxy()
            self.process_thread = None
        if self.verbose_printer is not None:
            self.verbose_printer.stop()
