import os
import subprocess
import utils


INTERFACE_BAT_PATH = os.path.join(
    os.path.relpath("assets"),
    "interface.bat"
)


def setup_windows_proxy(port):
    p1 = subprocess.Popen(
        'reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Internet Settings" /v ProxyEnable /t REG_DWORD /d 1 /f',
    )
    p2 = subprocess.Popen(
        f'reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Internet Settings" /v ProxyServer  /d "socks=127.0.0.1:{port};" /t REG_SZ /f'
    )
    p1.wait()
    p2.wait()


def setup_windows_dns():
    output = subprocess.Popen(
        INTERFACE_BAT_PATH,
        stdout=subprocess.PIPE).stdout
    interface_name = "Ethernet"
    for line in output:
        line = line.decode("utf-8")
        interface_name = line.replace("\n", "").replace("\r", "")
        break
    output.close()
    print(f"Setting DNS for interface: {interface_name}")
    subprocess.Popen(
        f'netsh interface ipv4 add dnsserver "{interface_name}" 127.0.0.1'
    ).wait()


def drop_windows_proxy():
    p1 = subprocess.Popen(
        'reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Internet Settings" /v ProxyEnable /t REG_DWORD /d 0 /f'
    )
    p2 = subprocess.Popen(
        f'reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Internet Settings" /v ProxyServer  /d "" /t REG_SZ /f',
    )
    p1.wait()
    p2.wait()


def drop_windows_dns():
    output = subprocess.Popen(
        INTERFACE_BAT_PATH,
        stdout=subprocess.PIPE).stdout
    interface_name = "Ethernet"
    for line in output:
        line = line.decode("utf-8")
        interface_name = line.replace("\n", "").replace("\r", "")
    p1 = subprocess.Popen(
        f'netsh interface ipv4 set dnsserver "{interface_name}" source=dhcp',
        shell=True
    )
    p1.wait()
    output.close()


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
                f"{self.get_process_path()}"
                f" -ssh {self.server} -D {self.socks_port} -l {self.username} -P {self.server_port} -no-antispoof -pw {self.password}"
                f" -T while true; do echo 0; sleep 30s; done"
            ],
            {
                "startupinfo": si,
            }
        )
        setup_windows_proxy(self.socks_port)
        setup_windows_dns()

    def stop(self):
        self.stopped = True
        self.subprocess.terminate()
        self.subprocess.wait()
        self.subprocess = None
        self.process_thread = None
        drop_windows_proxy()
        drop_windows_dns()
