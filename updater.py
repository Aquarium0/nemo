import os
import requests
import sys
from time import sleep
REPO_LINK = 'https://github.com/Aquarium0/nemo/blob/main/{}?raw=true'
VERSION_LINK = 'https://raw.githubusercontent.com/Aquarium0/nemo/main/version.json'

# name-vx.x

def checkUpdate():
    print("Checking for updates...")
    versions = requests.get(VERSION_LINK).json()
    curFile = sys.argv[0].split('\\')[-1].replace('.exe','').split('-')
    validFiles = [name for name in versions]

    for fileName in os.listdir(os.path.dirname(sys.executable)):
        appName = fileName.split('-')[0]
        if appName in validFiles and appName == curFile[0] and 'exe' in fileName:
            versionData = fileName.split('-')[1]
            if versionData[:-4] != versions[appName]:
                print(f"Found an update for {appName}. The program will download the update and automatically restart, please wait...")
                pullUpdate(f"{appName}-{versions[appName]}.exe")
                os.system(f"start {appName}-{versions[appName]}.exe")
                sleep(0.2)
                return True

def pullUpdate(fileName):
    fileData = requests.get(REPO_LINK.format(fileName))
    with open(fileName, 'wb') as f:
        f.write(fileData.content)
    
def checkPurge():
    versions = requests.get(VERSION_LINK).json()
    validFiles = [name for name in versions]
    curFile = sys.argv[0].split('\\')[-1].replace('.exe','').split('-')

    if versions[curFile[0]] != curFile[1]:
        return

    for fileName in os.listdir(os.path.dirname(sys.executable)):
        appName = fileName.split('-')[0]
        if appName in validFiles and 'exe' in fileName:
            versionData = fileName.split('-')[1]
            if versionData[:-4] != versions[appName]:
                os.remove(fileName)
                return True
