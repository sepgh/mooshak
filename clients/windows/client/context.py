import client


class ApplicationContext:
    instance = None

    @classmethod
    def get_instance(cls) -> "ApplicationContext":
        if cls.instance is None:
            cls.instance = ApplicationContext()
        return cls.instance

    def __init__(self):
        self.client = client.MooshakClient()
        self.interface_name = None

    def get_client(self):
        if self.client is None:
            client.MooshakClient()
        return self.client

    def set_interface_name(self, name):
        self.interface_name = name

    def get_interface_name(self):
        return self.interface_name

