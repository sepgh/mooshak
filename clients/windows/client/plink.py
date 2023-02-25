import os
import subprocess

from termcolor import cprint

from client import utils
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

    def get_process_path(self):
        return os.path.join(
            os.path.relpath("assets"),
            "plink.exe"
        )

    def start(self):
        if self.process_thread is not None:
            return

        si = subprocess.STARTUPINFO()
        si.dwFlags |= subprocess.STARTF_USESHOWWINDOW

        self.subprocess = subprocess.Popen(
            f"{self.get_process_path()} -hostkey {self.host_key} -ssh {self.server} -D {self.socks_port}"
            f" -l {self.username} -P {self.server_port} -no-antispoof -pw {self.password}"
            f" -N",
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            # startupinfo=si
        )
        cprint(f"Socks proxy available on {self.socks_port}", 'yellow')
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
