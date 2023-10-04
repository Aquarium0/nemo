import hashlib
import json
import sys

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

with open('version.json', "r") as f:
    temp = json.loads(f.read())

temp[file_name] = hash(f"{file_name}.exe")

json_object = json.dumps(temp, indent=2)

with open("version.json", "w") as outfile:
    outfile.write(json_object)
