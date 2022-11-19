import os
import time
import shutil
import requests

folder_to_process = r"D:\codrscrape\Output"
seven_zip_7z_exe = r"D:\codrscrape\7-Zip\7z.exe"
zip_array = []
unzipped_folder_array = []


def install_seven_zip(file_path):
    if not os.path.isfile(file_path):
        if not os.path.isdir((os.path.split(file_path))[0]):
            os.makedirs((os.path.split(file_path))[0])
        open(file_path, 'wb').write((requests.get("https://www.7-zip.org/a/7zr.exe", allow_redirects=True)).content)


def get_zip_files(folder_path):
    for root, dirs, files in os.walk(folder_path):
        for i in files:
            if i.endswith(".zip"):
                zip_array.append(os.path.join(root + "\\" + i))


def remove_old_unzipped(folder_path):
    for i3 in zip_array:
        i7 = (os.path.split(i3)[0]) + "\\" + "mod.zip_unzipped"
        if os.path.isdir(i7):
            shutil.rmtree(i7)
            print(i7 + " has been removed")


def unzip_zip_files():
    for i4 in zip_array:
        try:
            if os.path.isfile(i4):
                export_folder = i4 + "_unzipped"
                if not os.path.isdir(export_folder):
                    os.makedirs(export_folder)
                    os.system(seven_zip_7z_exe + " x" + " -y " + i4 + " -o" + export_folder)
                    print(i4 + " has extracted successfully")
                    unzipped_folder_array.append(i4)
                else:
                    print(i4 + " has already been extracted successfully")
        except:
            print(i4 + " failed to extract")
            time.sleep(60)


for i in unzipped_folder_array:
    for root, dirs, files, in os.walk(i):
        for i2 in dirs:
            print(i2)

get_zip_files(folder_to_process)
remove_old_unzipped(folder_to_process)
unzip_zip_files()

print()
print("Process Has Finished")
time.sleep(999999)

quit()
