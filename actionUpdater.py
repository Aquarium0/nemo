import hashlib
import json
import sys
import zipfile
import io
import shutil
import requests

generic_source = "https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/{}/win64/chromedriver-win64.zip"

def hash(file_path):
    h = hashlib.sha256()

    with open(file_path, 'rb') as file:
        while True:
            chunk = file.read(h.block_size)
            if not chunk:
                break
            h.update(chunk)

    return h.hexdigest()

file_name = sys.argv[1]

if file_name == "chromedriver":
    version_req = requests.get('https://googlechromelabs.github.io/chrome-for-testing/LATEST_RELEASE_STABLE', timeout=60)
    if version_req.status_code != 200:
        print("An error occurred in requesting the latest stable version, exiting early...")
        exit()
    
    version = version_req.text
    target_source = generic_source.format(version)

    zip_req = requests.get(target_source)
    zip = zipfile.ZipFile(io.BytesIO(zip_req.content))
    zip.extract("chromedriver-win64/chromedriver.exe")
    shutil.move("chromedriver-win64/chromedriver.exe", "chromedriver.exe")
    shutil.rmtree("chromedriver-win64")
else:
    with open('version.json', "r") as f:
        temp = json.loads(f.read())

    temp[file_name] = hash(f"{file_name}.exe")

    json_object = json.dumps(temp, indent=2)

    with open("version.json", "w") as outfile:
        outfile.write(json_object)
