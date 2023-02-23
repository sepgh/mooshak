import subprocess
import os


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

    def stop(self):
        self.subprocess.terminate()
        self.subprocess.wait()
        self.subprocess = None

