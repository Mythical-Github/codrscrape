import os
import stat
import time
import json
import shutil
import pathlib
import requests
import subprocess

exception_array = []
folder_to_process = r"D:\codrscrape\Output"
seven_zip_7z_exe = r"C:\Program Files\7-Zip\7z.exe"

link_list = {
    r"WaW Campaign Maps": r"https://callofdutyrepo.com/waw-campaign-maps/",
    r"Waw Zombie Maps": r"https://callofdutyrepo.com/wawmaps/",
    r"WaW Mods": r"https://callofdutyrepo.com/waw-mods/",
    r"BO1 Mods": r"https://callofdutyrepo.com/bo1-mods/",
    r"BO1 Maps": r"https://callofdutyrepo.com/bo1-maps-by-name/",
    #    r"BO3 Maps": r"https://callofdutyrepo.com/bo3-maps/",
    #    r"BO3 Mods": r"https://callofdutyrepo.com/bo3-zombie-mods/",
}


class CoDSpecific:

    @staticmethod
    def print_final():
        print()
        print("Files Have Finished Downloading")
        print()
        print("The Following Files If Any Had Problems Downloading/Parsing:")
        for exception in exception_array:
            print(exception)
        print()
        print("Wrapper Finished")

    @staticmethod
    def download_info():
        for link in link_list:
            path_arg = folder_to_process + "\\" + link.replace(" ", "_")
            archive_arg = f"{path_arg}\\Archive {link}.txt".replace(" ", "_")
            if not os.path.isdir(path_arg):
                os.makedirs(path_arg)
            subprocess.run(
                f"codrscrape.exe -l --path {path_arg} --archive {archive_arg} -w --to-screen {link_list.get(link)})")

    @staticmethod
    def download_mods(input_array):
        for metadata_json in input_array:
            if metadata_json.endswith("metadata.json"):
                file_path = f"{os.path.split(metadata_json)[0]}\\mod.zip"
                print()
                print(f"Checking if {file_path} Already Exists")
                if os.path.isfile(file_path):
                    print(f"{file_path} Already Exists")
                    print(f"Checking {file_path} Validity")
                    if does_file_begin_with_str(file_path, "<!-- Copyright"):
                        if os.path.isfile(file_path):
                            os.remove(file_path)
                            print("File Wasn't Valid, Checking Download Link")
                            if is_download_link_functional(get_item_from_json(metadata_json, "download")):
                                print("Download Link Functional, Re-downloading")
                                download_file(get_item_from_json(metadata_json, "download"), file_path)
                                print("File Downloaded")
                                if does_file_begin_with_str(file_path, "<!-- Copyright"):
                                    exception_array.append(file_path)
                            else:
                                print("Download Link Is Not Functional, Adding To Error Array")
                                exception_array.append(file_path)
                    else:
                        print("Mod Archive Is Valid")
                else:
                    print("Mod Archive Doesn't Currently Exist")
                    print("Checking Download Link Validity")
                    if is_download_link_functional(get_item_from_json(metadata_json, "download")):
                        print("Download Link Functional, Downloading")
                        download_file(get_item_from_json(metadata_json, "download"), file_path)
                        print("File Downloaded")
                        if not does_file_begin_with_str(file_path, "<!-- Copyright"):
                            exception_array.append(file_path)
                    else:
                        print("Download Link Is Not Functional, Adding To Error Array")
                        exception_array.append(file_path)

    @staticmethod
    def organize_unzipped_mods():
        for root, dirs, files in os.walk(folder_to_process):
            if r"$1" in root:
                if root.endswith(r"$1"):
                    if len(os.listdir(root)) == 0:
                        shutil.rmtree(root)
                    else:
                        print()
            if r"$PLUGINSDIR" in root:
                shutil.rmtree(root)
                print(f"{root} Was Removed")

    @staticmethod
    def extract_mod_archives():
        for file in get_files_by_extension_in_tree(folder_to_process, ".zip"):
            extract_archive(file, f"{file}_unzipped")


def does_file_begin_with_str(input_file: str, input_string: str) -> bool:
    # noinspection PyBroadException
    try:
        if open(input_file).read(len(input_string)) == input_string:
            pathlib.Path.unlink(pathlib.Path(input_file))
            return True
        else:
            os.remove(input_file)
            return True
    except:
        return False


def remove_readonly(func, path, _):
    os.chmod(path, stat.S_IWRITE)
    func(path)


def install_seven_zip():
    subprocess.run("winget install 7zip.7zip -h")


def get_files_by_extension_in_tree(input_dir: str, input_type: str) -> list:
    file_array = []
    for root, dirs, files in os.walk(input_dir):
        for file in files:
            if file.endswith(input_type):
                file_array.append(f"{root}\\{file}")
    return file_array


def extract_archive(input_archive: str, output_folder: str):
    if not os.path.isfile(seven_zip_7z_exe):
        install_seven_zip()
    try:
        if os.path.isfile(input_archive):
            if not os.path.isdir(output_folder):
                os.makedirs(output_folder)
                subprocess.run(f"{seven_zip_7z_exe} x -y {input_archive} -o{output_folder}")
                print(f"{input_archive} has extracted successfully")
            else:
                print(f"{input_archive} has already been extracted successfully")
        return True
    except Exception as ex:
        print(ex)
        print(f"{input_archive} failed to extract")


def del_files_by_ext_in_tree(input_dir: str, file_type: str):
    for root, dirs, files in os.walk(input_dir):
        for file in files:
            if file.endswith(file_type):
                pathlib.Path.unlink(pathlib.Path(f"{root}\\{file}"))


def is_download_link_functional(download_link: str) -> bool:
    try:
        if requests.get(download_link, allow_redirects=True).status_code == 200:
            return True
        else:
            return False
    except Exception as ex:
        print(ex)
        return False


def download_file(input_link: str, output_path: str):
    if input_link:
        open(output_path, 'wb').write(requests.get(input_link, allow_redirects=True).content)


def get_item_from_json(input_json: str, input_key: str) -> str:
    if os.path.isfile(input_json):
        with open(input_json, "r") as output_item:
            item = json.load(output_item)[input_key]
        return item
    else:
        exception_array.append(input_json)
        return "Failed To Obtain Download Link From Json"


def get_one_dir_up(input_dir: str) -> str:
    up_dir = ""
    return up_dir


CoDSpecific.download_info()
time.sleep(999999)
del_files_by_ext_in_tree(folder_to_process, ".tmp")
CoDSpecific.download_mods(get_files_by_extension_in_tree(folder_to_process, ".json"))
CoDSpecific.extract_mod_archives()
CoDSpecific.organize_unzipped_mods()
CoDSpecific.print_final()
time.sleep(999999)

quit()

# To Do List:
# get one dir up function
# finish organize_unzipped_mods
# Replace os module usage with pathlib module usage
# list incomplete entries and broken download links at end
# "use type hints and pass around Path objects instead of strings" look into this
