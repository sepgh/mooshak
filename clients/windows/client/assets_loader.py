import os

import requests
from termcolor import cprint


def download(url: str):
    assets_path = os.path.realpath("assets")
    if not os.path.exists(assets_path):
        os.makedirs(assets_path)  # create folder if it does not exist

    filename = url.split('/')[-1].replace(" ", "_")  # be careful with file names
    file_path = os.path.join(assets_path, filename)

    r = requests.get(url, stream=True)
    if r.ok:
        cprint(f"saving to {os.path.abspath(file_path)}", 'green')
        with open(file_path, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024 * 8):
                if chunk:
                    f.write(chunk)
                    f.flush()
                    os.fsync(f.fileno())
    else:  # HTTP status code 4XX/5XX
        cprint("Download failed: status code {}\n{}".format(r.status_code, r.text), 'red')


assets = [
    {
        "name": "DNS2SOCKS.exe",
        "url": "https://altushost-swe.dl.sourceforge.net/project/dns2socks/DNS2SOCKS.exe",
        "handler": lambda asset: download(asset["url"])
    },
    {
        "name": "plink.exe",
        "url": "https://the.earth.li/~sgtatham/putty/0.78/w64/plink.exe",
        "handler": lambda asset: download(asset["url"])
    },
    {
        "name": "wstunnel.exe",
        "url": "https://raw.githubusercontent.com/sepgh/mooshak/main/clients/windows/assets/wstunnel.exe",
        "handler": lambda asset: download(asset["url"])
    },
    {
        "name": "interface.bat",
        "url": "https://raw.githubusercontent.com/sepgh/mooshak/main/clients/windows/assets/interface.bat",
        "handler": lambda asset: download(asset["url"])
    },
]


def validate_assets():
    called_once = False
    for asset in assets:
        if not os.path.exists(
                os.path.join(os.path.relpath("assets"), asset["name"])
        ):
            called_once = True
            cprint(f"Could not find {asset['name']} in assets directory.", 'yellow')
            if 'handler' not in asset or asset.get('handler') is None:
                cprint("I can't download it for you. This may break the application. Skipping.")
                continue
            else:
                cprint(f"Downloading {asset['name']}")
                asset['handler'](asset)

    if not called_once:
        cprint("All assets are already loaded", "green")