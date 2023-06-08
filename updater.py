import os
import requests
import sys
from time import sleep
import hashlib
REPO_LINK = 'https://github.com/Aquarium0/nemo/blob/main/{}?raw=true'
VERSION_LINK = 'https://raw.githubusercontent.com/Aquarium0/nemo/main/version.json'

def hash(file_path):
    h = hashlib.sha256()

    with open(file_path, 'rb') as file:
        while True:
            chunk = file.read(h.block_size)
            if not chunk:
                break
            h.update(chunk)

    return h.hexdigest()
# name-vx.x

def checkUpdate():
    print("Checking for updates...")
    versions = requests.get(VERSION_LINK).json()
    curFile = sys.argv[0].split('\\')[-1].replace('.exe','')
    curFileHash = hash(sys.argv[0])

    if curFileHash != versions[curFile]:
        os.rename(sys.argv[0], sys.argv[0].split('.')[0] + '_OLDf07211be7a15041.exe')
        print(f"Found an update for {curFile}. The program will download the update and automatically restart, please wait...")
        pullUpdate(f"{curFile}.exe")
        os.system(f"start {curFile}.exe")
        sleep(0.2)
        return True

def pullUpdate(fileName):
    fileData = requests.get(REPO_LINK.format(fileName))
    with open(fileName, 'wb') as f:
        f.write(fileData.content)
    
def checkPurge():
    for fileName in os.listdir(os.path.dirname(sys.executable)):
        if '_OLDf07211be7a15041' in fileName:
            os.remove(fileName)
            return True


def updateConfirm():
    if getattr(sys, 'frozen', False):
        checkPurge()

        if checkUpdate():
            sys.exit()


if __name__ == "__main__":
    print(hash(input("Input File: ").replace("\"","")))