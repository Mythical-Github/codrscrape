import os
import wget
import time
import json

folder_to_process = r"D:\codrscrape\Output"
metadata_json_dict = {}

for root, dirs, files in os.walk(folder_to_process):
    for file in files:
        if file.endswith(".json"):
            metadata_json_dict[os.path.join(root, file)] = root

for i in metadata_json_dict:
    file_path = (metadata_json_dict[i] + "\\mod.zip")
    print()
    print(file_path)
    with open(i, "r") as read_file:
        data = json.load(read_file)
        response = wget.download(data["download"], out=file_path)

print()
print("Files Have Finished Downloading")

time.sleep(999999)

quit()
