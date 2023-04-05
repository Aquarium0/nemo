import os
import requests
import sys

REPO_LINK = 'https://github.com/Aquarium0/nemo/blob/main/{}?raw=true'
VERSION_LINK = 'https://raw.githubusercontent.com/Aquarium0/nemo/main/version.json'

VALID_FILES = ['AGM1', ]
# name-vx.x

def checkUpdate():
    versions = requests.get(VERSION_LINK).json()

    for fileName in os.listdir(os.path.dirname(sys.executable)):
        appName = fileName.split('-')[0]
        if appName in VALID_FILES and 'exe' in fileName:
            versionData = fileName.split('-')[1]
            if versionData[:-4] != versions[appName]:
                pullUpdate(f"{appName}-{versions[appName]}.exe")
                break

def pullUpdate(fileName):
    fileData = requests.get(REPO_LINK.format(fileName))
    with open(fileName, 'wb') as f:
        f.write(fileData.content)
    

def checkPurge():
    versions = requests.get(VERSION_LINK).json()

    for fileName in os.listdir(os.path.dirname(sys.executable)):
        appName = fileName.split('-')[0]
        if appName in VALID_FILES and 'exe' in fileName:
            versionData = fileName.split('-')[1]
            if versionData[:-4] != versions[appName]:
                os.remove(fileName)
                break
