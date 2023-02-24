import os
import subprocess

from termcolor import cprint

from client.win import setup_windows_dns, drop_windows_dns


class DNS2Socks:

    def __init__(self, port: int, dns_server: str, dns_server_port: int):
        self.port = port
        self.dns_server = dns_server
        self.dns_server_port = dns_server_port
        self.subprocess = None

    def get_process_path(self):
        return os.path.join(
            os.path.relpath("assets"),
            "DNS2SOCKS.exe"
        )

    def start(self):
        if self.subprocess is not None:
            return

        si = subprocess.STARTUPINFO()
        si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        self.subprocess = subprocess.Popen(
            f"{self.get_process_path()} 127.0.0.1:{str(self.port)} {self.dns_server}:{self.dns_server_port} 127.0.0.1:53",
            startupinfo=si,
        )
        cprint(f"DNS2Socks listening on 127.0.0.1:53. Primary DNS: {self.dns_server}:{self.dns_server_port}", "yellow")
        setup_windows_dns()

    def stop(self):
        if self.subprocess is not None:
            self.subprocess.terminate()
            self.subprocess.wait()
            self.subprocess = None
        drop_windows_dns()

