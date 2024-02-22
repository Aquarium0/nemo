import hashlib
import json
import sys
import zipfile
import io
import shutil
import requests

GENERIC_SOURCE = "https://storage.googleapis.com/chrome-for-testing-public/{}/win64/chromedriver-win64.zip"

def file_hash(file_path):
    """Returns the hash of a file."""
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
    version_req = requests.get(
        'https://googlechromelabs.github.io/chrome-for-testing/LATEST_RELEASE_STABLE',
        timeout=60
    )
    if version_req.status_code != 200:
        print("An error occurred in requesting the latest stable version, exiting early...")
        sys.exit()

    version = version_req.text
    target_source = GENERIC_SOURCE.format(version)

    zip_req = requests.get(target_source, timeout=60)
    zip_file = zipfile.ZipFile(io.BytesIO(zip_req.content))
    zip_file.extract("chromedriver-win64/chromedriver.exe")
    shutil.move("chromedriver-win64/chromedriver.exe", "chromedriver.exe")
    shutil.rmtree("chromedriver-win64")

    with open('version.json', "r", encoding="locale") as f:
        temp = json.loads(f.read())

    temp['chromedriver'] = version

    json_object = json.dumps(temp, indent=2)

    with open("version.json", "w", encoding="locale") as outfile:
        outfile.write(json_object)

else:
    with open('version.json', "r", encoding="locale") as f:
        temp = json.loads(f.read())

    temp[file_name] = file_hash(f"{file_name}.exe")

    json_object = json.dumps(temp, indent=2)

    with open("version.json", "w", encoding="locale") as outfile:
        outfile.write(json_object)
