from nubia import command
from termcolor import cprint

from client import assets_loader
from client.context import ApplicationContext


@command()
def update_assets():
    """Validates and updates assets if possible"""
    assets_loader.validate_assets()


@command()
def start():
    """Connect to Mooshak server"""
    ApplicationContext.get_instance().get_client().start()
    cprint("Connection initiated ...", "green")


@command()
def stop():
    """Disconnect from Mooshak server"""
    ApplicationContext.get_instance().get_client().stop()
    cprint("Connection stopped ...", "yellow")

