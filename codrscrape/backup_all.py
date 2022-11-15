import os
import time

link_list = {
    r"WaW Campaign Maps": r"https://callofdutyrepo.com/waw-campaign-maps/",
    r"Waw Zombie Maps": r"https://callofdutyrepo.com/wawmaps/",
    r"WaW Mods": r"https://callofdutyrepo.com/waw-mods/",
    r"BO1 Mods": r"https://callofdutyrepo.com/bo1-mods/",
    r"BO1 Maps": r"https://callofdutyrepo.com/bo1-maps-by-name/",
    r"BO3 Maps": r"https://callofdutyrepo.com/bo3-maps/",
    r"BO3 Mods": r"https://callofdutyrepo.com/bo3-zombie-mods/",
}

for i in link_list:
    path_arg = "Output\\" + i.replace(" ", "_")
    archive_arg = path_arg + ("\Archive " + i + ".txt").replace(" ", "_")
    if not os.path.isdir(path_arg):
        os.makedirs(path_arg)
    os.system("codrscrape.exe -l --path " + path_arg + " --archive " + archive_arg + " -w " + " --to-screen " + link_list.get(i))

time.sleep(999999)

quit()
