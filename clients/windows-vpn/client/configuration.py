import os.path

DEFAULT_CONFIGURATION_PATHS = ["client.json"]  # Default paths to read the configuration from


def get_configuration(arg_config: str = None):
    """
    Loads json configuration of server
    """

    if arg_config is not None and os.path.exists(arg_config):
        return arg_config

    for conf in DEFAULT_CONFIGURATION_PATHS:
        if os.path.exists(conf):
            return conf
