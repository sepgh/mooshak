import os
import subprocess

from termcolor import cprint

from client.context import ApplicationContext

INTERFACE_BAT_PATH = os.path.join(
    os.path.relpath("assets"),
    "interface.bat"
)


def setup_windows_proxy(port):
    p1 = subprocess.Popen(
        'reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Internet Settings" /v ProxyEnable /t REG_DWORD /d 1 /f',
        stdout=subprocess.DEVNULL,
        stderr=subprocess.STDOUT,

    )
    p2 = subprocess.Popen(
        f'reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Internet Settings" /v ProxyServer  /d "socks=127.0.0.1:{port};" /t REG_SZ /f',
        stdout=subprocess.DEVNULL,
        stderr=subprocess.STDOUT,

    )
    p1.wait()
    p2.wait()


def get_interface_name():
    v = ApplicationContext.get_instance().get_interface_name()
    if v is not None:
        return v

    interface_sub_process = subprocess.Popen(
        INTERFACE_BAT_PATH,
        stdout=subprocess.PIPE
    )
    output = interface_sub_process.stdout
    interface_name = "Ethernet"
    for line in output:
        line = line.decode("utf-8")
        interface_name = line.replace("\n", "").replace("\r", "")
        break
    output.close()
    interface_sub_process.terminate()
    interface_sub_process.wait()
    ApplicationContext.get_instance().set_interface_name(interface_name)
    return interface_name


def setup_windows_dns():
    interface_name = get_interface_name()
    cprint(f"Setting DNS for interface: {interface_name}", "yellow")
    subprocess.Popen(
        f'netsh interface ipv4 add dnsserver "{interface_name}" 127.0.0.1',
        stdout=subprocess.DEVNULL,
        stderr=subprocess.STDOUT,

    ).wait()


def drop_windows_proxy():
    p1 = subprocess.Popen(
        'reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Internet Settings" /v ProxyEnable /t REG_DWORD /d 0 /f',
        stdout=subprocess.DEVNULL,
        stderr=subprocess.STDOUT,
    )
    p2 = subprocess.Popen(
        f'reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Internet Settings" /v ProxyServer  /d "" /t REG_SZ /f',
        stdout=subprocess.DEVNULL,
        stderr=subprocess.STDOUT,

    )
    p1.wait()
    p2.wait()


def drop_windows_dns():
    interface_name = get_interface_name()
    p1 = subprocess.Popen(
        f'netsh interface ipv4 set dnsserver "{interface_name}" source=dhcp',
        stdout=subprocess.DEVNULL,
        stderr=subprocess.STDOUT,

    )
    p1.wait()

