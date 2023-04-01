import os
import subprocess

from client.context import ApplicationContext

INTERFACE_BAT_PATH = os.path.join(
    os.path.relpath("assets"),
    "interface.bat"
)


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

