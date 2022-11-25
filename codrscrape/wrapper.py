import glob
import stat
import time
import json
import shutil
import pathlib
import requests
import subprocess

exception_array = []

DIR_TO_PROCESS = pathlib.Path(r"D:\codrscrape\Output")
SEVEN_ZIP_7Z_EXE = r"C:\Program Files\7-Zip\7z.exe"
LINK_LIST = {
    r"WaW Campaign Maps": r"https://callofdutyrepo.com/waw-campaign-maps/",
    #    r"Waw Zombie Maps": r"https://callofdutyrepo.com/wawmaps/",
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
    def download_info(input_dir: pathlib.Path):
        for link in LINK_LIST:
            path = pathlib.Path(input_dir)
            archive = pathlib.Path(f"{path}\\Archive {link}.txt".replace(" ", "_"))
            if not pathlib.Path.is_dir(path):
                pathlib.Path.mkdir(path)
            subprocess.run(f"codrscrape.exe -l --path {path} --archive {archive} -w --to-screen {LINK_LIST.get(link)})")

    @staticmethod
    def download_mods(input_array):
        for json_ in input_array:
            if str(json_).endswith("metadata.json"):
                file_path = pathlib.Path(f"{get_one_dir_up(json_)}\\mod.zip")
                print()
                print(f"Checking if {file_path} Already Exists")
                if pathlib.Path.is_file(file_path):
                    print(f"{file_path} Already Exists")
                    print(f"Checking {file_path} Validity")
                    if does_file_begin_with_str(file_path, "<!-- Copyright"):
                        if pathlib.Path.is_file(file_path):
                            pathlib.Path.unlink(file_path)
                            print("File Wasn't Valid, Checking Download Link")
                            if is_download_link_functional(get_item_from_json(json_, "download")):
                                print("Download Link Functional, Re-downloading")
                                download_file(get_item_from_json(json_, "download"), file_path)
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
                    if is_download_link_functional(get_item_from_json(json_, "download")):
                        print("Download Link Functional, Downloading")
                        download_file(get_item_from_json(json_, "download"), file_path)
                        print("File Downloaded")
                        if not does_file_begin_with_str(file_path, "<!-- Copyright"):
                            exception_array.append(file_path)
                    else:
                        print("Download Link Is Not Functional, Adding To Error Array")
                        exception_array.append(file_path)

    @staticmethod
    def organize_unzipped_mods(input_dir: pathlib.Path):
        for file in get_files_by_extension_in_tree(input_dir, "$1"):
            if str(file).endswith(r"$1"):
                if is_dir_empty(file):
                    shutil.rmtree(file)
                else:
                    try:
                        shutil.move(pathlib.Path(file), get_one_dir_up(file))
                    except Exception as FailedOrganizationError:
                        return FailedOrganizationError
        for file in get_files_by_extension_in_tree(input_dir, "$PLUGINSDIR"):
            shutil.rmtree(file)

    @staticmethod
    def extract_mod_archives(input_dir: pathlib.Path):
        for file in get_files_by_extension_in_tree(input_dir, ".zip"):
            extract_archive(file, pathlib.Path(f"{file}_unzipped"))


def does_file_begin_with_str(input_file: pathlib.Path, input_string: str) -> bool:
    # noinspection PyBroadException
    try:
        if open(input_file).read(len(input_string)) == input_string:
            pathlib.Path.unlink(pathlib.Path(input_file))
            return True
        else:
            pathlib.Path.unlink(input_file)
            return True
    except:
        return False


def remove_readonly(func, path, _):
    pathlib.Path.chmod(path, stat.S_IWRITE)
    func(path)


def install_seven_zip():
    subprocess.run("winget install 7zip.7zip -h")


def get_files_by_extension_in_tree(input_dir: pathlib.Path, input_type: str) -> list:
    file_array = []
    for file in glob.glob(f"{input_dir}/**/*{input_type}", recursive=True):
        file_array.append(pathlib.Path(file))
    return file_array


def extract_archive(input_archive: pathlib.Path, output_folder: pathlib.Path):
    if not pathlib.Path(SEVEN_ZIP_7Z_EXE):
        install_seven_zip()
    try:
        if pathlib.Path.is_file(input_archive):
            if not pathlib.Path.is_dir(output_folder):
                pathlib.Path.mkdir(output_folder)
                subprocess.run(f"{SEVEN_ZIP_7Z_EXE} x -y {input_archive} -o{output_folder}")
                print(f"{input_archive} has extracted successfully")
            else:
                print(f"{input_archive} has already been extracted successfully")
        return True
    except Exception as FailedExtractionError:
        print(FailedExtractionError)
        print(f"{input_archive} failed to extract")


def del_files_by_ext_in_tree(input_dir: pathlib.Path, file_type: str):
    for i in get_files_by_extension_in_tree(input_dir, file_type):
        pathlib.Path.unlink(i)


def is_download_link_functional(download_link: str) -> bool:
    try:
        if requests.get(download_link, allow_redirects=True).status_code == 200:
            return True
        else:
            return False
    except Exception as DownloadLinkNotFunctionError:
        print(DownloadLinkNotFunctionError)
        return False


def download_file(input_link: str, output_path: pathlib.Path):
    if input_link:
        open(output_path, 'wb').write(requests.get(str(input_link), allow_redirects=True).content)


def get_item_from_json(input_json: pathlib.Path, input_key: str) -> str:
    if pathlib.Path.is_file(input_json):
        with open(input_json, "r") as output_item:
            item = json.load(output_item)[input_key]
        return item
    else:
        exception_array.append(input_json)
        return "Failed To Obtain Download Link From Json"


def get_one_dir_up(input_dir: pathlib.Path) -> pathlib.Path:
    return pathlib.Path(input_dir).parents[0]


def is_dir_empty(input_dir: pathlib.Path) -> bool:
    initial_count = 0
    for path in input_dir.iterdir():
        if path.is_file():
            initial_count += 1
    if initial_count == 0:
        return True
    else:
        return False


CoDSpecific.download_info(DIR_TO_PROCESS)
del_files_by_ext_in_tree(DIR_TO_PROCESS, ".tmp")
CoDSpecific.download_mods(get_files_by_extension_in_tree(DIR_TO_PROCESS, "metadata.json"))
CoDSpecific.extract_mod_archives(DIR_TO_PROCESS)
CoDSpecific.organize_unzipped_mods(DIR_TO_PROCESS)
CoDSpecific.print_final()
time.sleep(999999)
quit()


# To Do List:
# finish organize_unzipped_mods
