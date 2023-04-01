import requests
from  requests.exceptions import ConnectionError, ConnectTimeout
from termcolor import cprint

from client.utils import retry_on_false


def test_socks(url, host="127.0.0.1", port=6060, timeout=10):
    try:
        resp = requests.get(
            url,
            timeout=timeout,
            proxies=dict(
                http=f'socks5h://{host}:{port}',
                https=f'socks5h://{host}:{port}'
            )
        )
        if resp.status_code == 200:
            return True
        return False
    except (ConnectionError, ConnectTimeout):
        return False


def test_socks_default(host="127.0.0.1", port=6060, timeout=10):
    try:
        resp = requests.get(
            "http://ifconfig.me",
            timeout=timeout,
            proxies=dict(
                http=f'socks5h://{host}:{port}',
                https=f'socks5h://{host}:{port}'
            )
        )
        if resp.status_code == 200:
            cprint(f"IP Check Response: {resp.text}", "yellow")
            return True
        return False
    except (ConnectionError, ConnectTimeout):
        return False


class SocksTester:
    def __init__(self, configuration: dict):
        self.configuration = configuration
        self.test_url = self.configuration.get("test_url")
        self.test_retry_count = self.configuration.get("test_retry_count", 5)
        self.test_timeout = self.configuration.get("test_url", 5)
        self.test_func = None
        self.test_args = None
        self.test_kwargs = None
        if self.test_url is None:
            self.test_func = test_socks_default
            self.test_kwargs = {
                "port": self.configuration.get("socks_port", 6060)
            }
        else:
            self.test_func = test_socks
            self.test_kwargs = {
                "url": self.test_url,
                "port": self.configuration.get("socks_port", 6060)
            }

    def test(self):
        if not self.configuration.get("test", True):
            return True
        cprint("Running SOCKS Test", "yellow")
        result = retry_on_false(
            self.test_retry_count,
            self.test_func,
            kwargs=self.test_kwargs
        )
        if result is False:
            cprint("Socks test failed", "red")
        return result
