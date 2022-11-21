import os
import time
import json
import shutil
import requests
import subprocess

metadata_json_dict = {}
exception_array = []
folder_to_process = r"D:\codrscrape\Output"
seven_zip_7z_exe = r"D:\codrscrape\7-Zip\7z.exe"
zip_array = []
unzipped_folder_array = []

link_list = {
    #    r"WaW Campaign Maps": r"https://callofdutyrepo.com/waw-campaign-maps/",
    #    r"Waw Zombie Maps": r"https://callofdutyrepo.com/wawmaps/",
    #    r"WaW Mods": r"https://callofdutyrepo.com/waw-mods/",
    r"BO1 Mods": r"https://callofdutyrepo.com/bo1-mods/",
    r"BO1 Maps": r"https://callofdutyrepo.com/bo1-maps-by-name/",
    #    r"BO3 Maps": r"https://callofdutyrepo.com/bo3-maps/",
    #    r"BO3 Mods": r"https://callofdutyrepo.com/bo3-zombie-mods/",
}


def up_one_directory(input_path):
    head, tail = os.path.split(input_path)
    try:
        shutil.move(input_path, os.path.join(os.path.split(head)[0], tail))
    except Exception as ex:
        print(ex)
        pass


def install_seven_zip():
    subprocess.run("winget install 7zip.7zip")


def get_zip_files(folder_path):
    for root, dirs, files in os.walk(folder_path):
        for i in files:
            if i.endswith(".zip"):
                zip_array.append(os.path.join(f"{root}\\{i}"))


def remove_old_unzipped():
    for mod_zip in zip_array:
        unzipped_folder = f"{(os.path.split(mod_zip)[0])}\\mod.zip_unzipped"
        if os.path.isdir(unzipped_folder):
            shutil.rmtree(unzipped_folder)
            print(f"{unzipped_folder} has been removed")


def unzip_zip_files():
    for mod_zip in zip_array:
        try:
            if os.path.isfile(mod_zip):
                export_folder = f"{mod_zip}_unzipped"
                if not os.path.isdir(export_folder):
                    os.makedirs(export_folder)
                    subprocess.run(f"{seven_zip_7z_exe} x -y {mod_zip} -o{export_folder}")
                    print(f"{mod_zip} has extracted successfully")
                    unzipped_folder_array.append(mod_zip)
                else:
                    print(f"{mod_zip} has already been extracted successfully")
        except Exception as ex:
            print(ex)
            print(f"{mod_zip} failed to extract")


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
    except Exception as ex:
        print(ex)
        return False


def is_valid_mod_archive(input_file):
    # noinspection PyBroadException
    try:
        if open(input_file).read(14) == "<!-- Copyright":
            os.remove(input_file)
            return False
        else:
            #              not sure why this was here
            #            os.remove(input_file)
            return True
    except:
        return True


def download_file(download_link, output_path):
    if download_link:
        open(output_path, 'wb').write(requests.get(download_link, allow_redirects=True).content)


def get_json_files_in_dir(input_dir):
    for root, dirs, files in os.walk(input_dir):
        for file in files:
            full_path = os.path.join(root, file)
            if file.endswith(".json"):
                if "unzipped" not in root:
                    metadata_json_dict[full_path] = root


def get_download_link_from_json(input_file):
    if os.path.isfile(input_file):
        with open(input_file, "r") as output_file:
            download_link = json.load(output_file)["download"]
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


def organize_unzipped_files():
    for root, dirs, files in os.walk(folder_to_process):
        if r"$1" in root:
            if root.endswith(r"$1"):
                if len(os.listdir(root)) == 0:
                    shutil.rmtree(root)
                else:
                    up_one_directory(folder_to_process)
        if r"$PLUGINSDIR" in root:
            shutil.rmtree(root)
            print(f"{root} Was Removed")


def download_info():
    for i in link_list:
        path_arg = folder_to_process + "\\" + i.replace(" ", "_")
        archive_arg = f"{path_arg}\\Archive {i}.txt".replace(" ", "_")
        if not os.path.isdir(path_arg):
            os.makedirs(path_arg)
        subprocess.run(
            f"codrscrape.exe -l --path {path_arg} --archive {archive_arg} -w --to-screen {link_list.get(i)})")


def download_mods():
    for i in metadata_json_dict:
        file_path = f"{metadata_json_dict[i]}\\mod.zip"
        print()
        print(f"Checking if {file_path} Already Exists")
        if os.path.isfile(file_path):
            print(f"{file_path} Already Exists")
            print(f"Checking {file_path} Validity")
            if not is_valid_mod_archive(file_path):
                if os.path.isfile(file_path):
                    os.remove(file_path)
                    print("File Wasn't Valid, Checking Download Link")
                    if is_download_link_functional(get_download_link_from_json(i)):
                        print("Download Link Functional, Re-downloading")
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
            print("Mod Archive Doesn't Currently Exist")
            print("Checking Download Link Validity")
            if is_download_link_functional(get_download_link_from_json(i)):
                print("Download Link Functional, Downloading")
                download_file(get_download_link_from_json(i), file_path)
                print("File Downloaded")
                if not is_valid_mod_archive(file_path):
                    exception_array.append(file_path)
            else:
                print("Download Link Is Not Functional, Adding To Error Array")
                exception_array.append(file_path)


download_info()
del_files_of_type_in_dir(folder_to_process, ".tmp")
get_json_files_in_dir(folder_to_process)
download_mods()
print_final()
get_zip_files(folder_to_process)
remove_old_unzipped()
unzip_zip_files()
print()
organize_unzipped_files()
print()
print("Wrapper Finished")
time.sleep(999999)

quit()

# To Do List:
# Replace os module usage with pathlib module usage
