import os
import sys
from time import sleep
import hashlib

import requests

REPO_LINK = "https://github.com/Aquarium0/nemo/blob/main/{}?raw=true"
VERSION_LINK = "https://raw.githubusercontent.com/Aquarium0/nemo/main/version.json"


def updater_hash(file_path):
    """Returns the sha256 hash of a file."""
    h = hashlib.sha256()

    with open(file_path, "rb") as file:
        while True:
            chunk = file.read(h.block_size)
            if not chunk:
                break
            h.update(chunk)

    return h.hexdigest()


def check_update():
    """Checks if there is an update for the program, if so, it will download and install it."""
    print("Checking for updates...")
    versions = requests.get(VERSION_LINK, timeout=120).json()
    cur_file = sys.argv[0].split("\\")[-1].replace(".exe", "").split(" ")[0]
    cur_file_hash = updater_hash(sys.argv[0])

    if cur_file_hash != versions[cur_file]:
        os.rename(sys.argv[0], sys.argv[0] + "_OLDf07211be7a15041.exe")
        print(
            f"Found an update for {cur_file}. The program will download "
            "the update and automatically restart, please wait..."
        )
        pull_update(f"{cur_file}.exe")
        additional = f" {' '.join(sys.argv[1:])}" if len(sys.argv) > 1 else ""
        os.system(f"start {cur_file}.exe{additional}")
        sleep(0.2)
        return True
    return False

def pull_update(file_name):
    """Downloads the update from the GitHub repo."""
    file_data = requests.get(REPO_LINK.format(file_name), timeout=120)
    with open(file_name, "wb") as f:
        f.write(file_data.content)


def check_purge():
    """Checks if there is an old version of the program and deletes it, if so."""
    for file_name in os.listdir(os.path.dirname(sys.executable)):
        if "_OLDf07211be7a15041" in file_name:
            os.remove(file_name)


def update_confirm():
    """Checks whether an update exists and if so, runs updaters."""
    if getattr(sys, "frozen", False):
        check_purge()

        if check_update():
            sys.exit()


if __name__ == "__main__":
    print(updater_hash(input("Input File: ").replace('"', "")))
