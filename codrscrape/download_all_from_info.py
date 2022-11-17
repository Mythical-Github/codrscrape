import os
import time
import json
import requests

folder_to_process = r"D:\codrscrape\Output"
metadata_json_dict = {}
exception_array = []
files_to_remove_array = []

for root, dirs, files in os.walk(folder_to_process):
    for file in files:
        full_path = os.path.join(root, file)
        if file.endswith(".zip") or file.endswith(".tmp"):
            files_to_remove_array.append(full_path)
        if file.endswith(".json"):
            metadata_json_dict[full_path] = root

for i in files_to_remove_array:
    os.remove(i)
    print("Old File " + i + " Was Removed")

for i in metadata_json_dict:
    file_path = (metadata_json_dict[i] + "\\mod.zip")
    print()
    print(file_path)
    with open(i, "r") as read_file:
        try:
            data = json.load(read_file)
            test = data["download"]
            r = requests.get(test, allow_redirects=True)
            if r.status_code == 200:
                print("Mod Download Link is Functional")
                open(file_path, 'wb').write(r.content)
            else:
                print("Mod Download Link is NOT Functional")
                exception_array.append(file_path)
        except:
            print("Mod Download Link is NOT Functional")
            exception_array.append(file_path)


print()
print("Files Have Finished Downloading")
print()
print("The Following Files Had Problems Downloading:")
for i in exception_array:
    print(i)
print()
print("Process Complete")

time.sleep(999999)

quit()
