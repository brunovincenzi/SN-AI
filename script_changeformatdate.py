import json
from datetime import datetime

file_path = "./json_files/train/SerieA_1617_copy.json"

# carica il JSON
with open(file_path, "r") as f:
    data = json.load(f)

# conversione formato data
for match in data:
    dt = datetime.strptime(match["DateUtc"], "%m/%d/%y %H:%M")
    match["DateUtc"] = dt.strftime("%Y-%m-%d %H:%M:%SZ")

# sovrascrive il file
with open(file_path, "w") as f:
    json.dump(data, f, indent=4)

print("Date convertite e file sovrascritto.")