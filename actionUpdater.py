import hashlib
import json
def hash(file_path):
    h = hashlib.sha256()

    with open(file_path, 'rb') as file:
        while True:
            chunk = file.read(h.block_size)
            if not chunk:
                break
            h.update(chunk)

    return h.hexdigest()

with open('version.json', "r") as f:
    temp = json.loads(f.read())

temp['TourplanDailyBanking'] = hash("TourplanDailyBanking.exe")

json_object = json.dumps(temp, indent=2)

with open("version.json", "w") as outfile:
    outfile.write(json_object)
