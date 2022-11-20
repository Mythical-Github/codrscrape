import os
import time
import json
import requests

folder_to_process = r"D:\codrscrape\Output"
metadata_json_dict = {}
exception_array = []


def del_files_of_type_in_dir(input_dir, file_type):
    for root, dirs, files in os.walk(input_dir):
        for file in files:
            if file.endswith(file_type):
                os.remove(os.path.join(root, file))


def is_download_link_functional(download_link):
    try:
        if requests.get(download_link, allow_redirects=True).status_code == 200:
            return True
        else:
            return False
    except:
        return False


def is_valid_mod_archive(input_file):
    try:
        if open(input_file).read(14) == "<!-- Copyright":
            os.remove(input_file)
            return False
        else:
            os.remove(file_path)
            return True
    except:
        return True


def download_file(download_link, output_path):
    if not download_link == False:
        open(output_path, 'wb').write(requests.get(download_link, allow_redirects=True).content)


def get_json_files_in_dir(input_dir):
    for root, dirs, files in os.walk(input_dir):
        for file in files:
            full_path = os.path.join(root, file)
            if file.endswith(".json"):
                metadata_json_dict[full_path] = root


def get_download_link_from_json(input_file):
    if os.path.isfile(input_file):
        with open(i, "r") as input_file:
            download_link = json.load(input_file)["download"]
            return download_link
    else:
        exception_array.append(input_file)
        return False


def print_final():
    print()
    print("Files Have Finished Downloading")
    print()
    print("The Following Files If Any Had Problems Downloading:")
    for i in exception_array:
        print(i)
    print()
    print("Process Complete")


del_files_of_type_in_dir(folder_to_process, ".tmp")
get_json_files_in_dir(folder_to_process)


for i in metadata_json_dict:
    file_path = (metadata_json_dict[i] + "\\mod.zip")
    print()
    print("Checking if " + file_path + " Already Exists")
    print(file_path)
    if os.path.isfile(file_path):
        print(file_path + " Already Exists")
        print("Checking " + file_path + " Validity")
        if not is_valid_mod_archive(file_path):
            if os.path.isfile(file_path):
                os.remove(file_path)
                print("File Wasn't Valid, Checking Download Link")
                if is_download_link_functional(get_download_link_from_json(i)):
                    print("Download Link Functional, Redownloading")
                    download_file(get_download_link_from_json(i), file_path)
                    print("File Downloaded")
                    if not is_valid_mod_archive(file_path):
                        exception_array.append(file_path)
                else:
                    print("Download Link Is Not Functional, Adding To Error Array")
                    exception_array.append(file_path)
        else:
            print("Mod Archive Is Valid")
    else:
        print("Mod.zip Doesn't Currently Exist")
        print("Checking Download Link Validity")
        if is_download_link_functional(get_download_link_from_json(i)):
            print("Download Link Functional, Downloading")
            download_file(get_download_link_from_json(i), file_path)
            print("File Downloaded")
        else:
            print("Download Link Is Not Functional, Adding To Error Array")
            exception_array.append(file_path)

print_final()
time.sleep(999999)

quit()

