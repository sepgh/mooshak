import os
import subprocess

from termcolor import cprint

from client import utils
from client.win import setup_windows_proxy, setup_windows_dns, drop_windows_proxy, drop_windows_dns


class PLink:
    max_retries = 5

    def __init__(self, socks_port: int, server: str, server_port: int, username: str, password: str, on_interrupt=None):
        self.socks_port = socks_port
        self.server = server
        self.server_port = server_port
        self.username = username
        self.password = password
        self.process_thread = None
        self.subprocess = None
        self.current_retries = 0
        self.stopped = False
        self.on_interrupt = on_interrupt

    def get_process_path(self):
        return os.path.join(
            os.path.relpath("assets"),
            "plink.exe"
        )

    def set_process(self, process):
        self.subprocess = process

    def _on_exit(self):
        if self.current_retries != self.max_retries and not self.stopped:
            cprint("Disconnected from server. Retrying ...", "red")
            self.start()
        elif not self.stopped:
            self.stop()
            self.on_interrupt()

    def start(self):
        self.stopped = False
        if self.process_thread is not None:
            return

        si = subprocess.STARTUPINFO()
        si.dwFlags |= subprocess.STARTF_USESHOWWINDOW

        self.process_thread = utils.popen_and_call(
            self._on_exit,
            self.set_process,
            [
                f" -ssh {self.server} -D {self.socks_port} -l {self.username} -P {self.server_port} -no-antispoof -pw {self.password}"
                f" -N"
            ],
            {
                "executable": f"{self.get_process_path()}",
                "stdout": subprocess.PIPE,
                "stderr": subprocess.DEVNULL,
                "startupinfo": si,
            }
        )
        setup_windows_proxy(self.socks_port)
        setup_windows_dns()

    def stop(self):
        self.stopped = True
        if self.subprocess is not None:
            self.subprocess.terminate()
            self.subprocess.wait()
            self.subprocess = None
        drop_windows_proxy()
        drop_windows_dns()
        self.process_thread = None
