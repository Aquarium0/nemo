import os
import requests
import sys

REPO_LINK = 'https://github.com/Aquarium0/nemo/blob/main/{}?raw=true'
VERSION_LINK = 'https://raw.githubusercontent.com/Aquarium0/nemo/main/version.json'

# name-vx.x

def checkUpdate():
    versions = requests.get(VERSION_LINK).json()
    validFiles = [name for name in versions]

    for fileName in os.listdir(os.path.dirname(sys.executable)):
        appName = fileName.split('-')[0]
        if appName in validFiles and 'exe' in fileName:
            versionData = fileName.split('-')[1]
            if versionData[:-4] != versions[appName]:
                pullUpdate(f"{appName}-{versions[appName]}.exe")
                return True

def pullUpdate(fileName):
    fileData = requests.get(REPO_LINK.format(fileName))
    with open(fileName, 'wb') as f:
        f.write(fileData.content)
    

def checkPurge():
    versions = requests.get(VERSION_LINK).json()
    validFiles = [name for name in versions]

    for fileName in os.listdir(os.path.dirname(sys.executable)):
        appName = fileName.split('-')[0]
        if appName in validFiles and 'exe' in fileName:
            versionData = fileName.split('-')[1]
            if versionData[:-4] != versions[appName]:
                os.remove(fileName)
                return False
