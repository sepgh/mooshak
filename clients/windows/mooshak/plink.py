import os
import subprocess
import utils


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

    def _on_exit(self):
        if self.current_retries != self.max_retries and not self.stopped:
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

        def set_process(process):
            self.subprocess = process

        self.process_thread = utils.popen_and_call(
            self._on_exit,
            set_process,
            [
                f"{self.get_process_path()}"
                f" -ssh {self.server} -D 6060 -l {self.username} -P %{self.server_port} -no-antispoof -pw {self.password}"
                f" -T while true; do echo 0; sleep 30s; done"
            ],
            {
                "startupinfo": si
            }
        )

    def stop(self):
        self.stopped = True
        self.subprocess.terminate()
        self.subprocess.wait()
        self.subprocess = None
        self.process_thread = None
