#!/usr/bin/env python3

from zipfile import ZipFile
from sys import argv, platform
from os import chdir, path, makedirs
from subprocess import Popen
import os

# Stellaris mod folder path for the GOG version of the game
linux = platform == "linux" or platform == "linux2"
darwin = platform == "darwin"
windows = platform == "win32" or platform == "win64"
if darwin:
    # Mac OS
    mod_path = "/Documents/Paradox Interactive/Stellaris/mod"
elif windows:
    # Windows
    mod_path = "\\Documents\\Paradox Interactive\\Stellaris\\mod"
else:
    # Linux
    mod_path = "/.local/share/Paradox Interactive/Stellaris/mod"


# expected full user mod path
usr_mod_path = path.expanduser("~") + mod_path

# test.zip path, only for testing, this is obsolute!
# mod_zip = path.expanduser("~") + "\\Downloads\\test_mod.zip"


def find_mod_folder():
    # change dir to mod folder if it exists, if not create it
    if path.exists(usr_mod_path):
        chdir(usr_mod_path)

    else:
        try:
            makedirs(usr_mod_path)
        except OSError:
            print("failed creating mod folder!")


def unzip_mod_zip():
    # check if zip contains .mod file and extract, if not, quit
    found = False
    with ZipFile(mod_zip, "r") as zipfile:

        global zip_list
        zip_list = zipfile.namelist()

        for item in zip_list:
            if item.endswith(".mod"):
                zipfile.extractall(usr_mod_path)
                found = True
                print("zip extracted to " + usr_mod_path)
                break

    if not found:
        print("zip doesnt contain .mod file!")
        print("quitting now...")
        quit()


def modify_dot_mod():
    # assign 2nd item from previous list to a var and modify the file
    global dot_mod
    dot_mod = zip_list[1]

    # NOTE(jq): Not sure if needed, test if '/' works on Windows
    if windows:
        f = open(usr_mod_path + "\\" + dot_mod, "r+")
    else:
        # MacOS or Linux NOTE(jq): not test on MacOS
        f = open(usr_mod_path + "/" + dot_mod, "r+")

    try:
        dm_c = f.read()
        rp_start = "path=\""
        rp_end = zip_list[2]
        to_rp = dm_c[dm_c.find(rp_start)+len(rp_start):dm_c.rfind(rp_end)]
        dm_c = dm_c.replace(to_rp, "mod/")
        f.seek(0)
        f.truncate(0)
        f.flush()
        f.write(dm_c)
        print(".mod successfully edited!")

    except Exception as e:
        print(e)

    finally:
        if f is not None:
            f.close()


def open_path():
    if windows:
        os.startfile(usr_mod_path)
    elif darwin:
        Popen(["open", usr_mod_path])
    else:
        Popen(["xdg-open", usr_mod_path])


if __name__ == "__main__":

    try:
        global mod_zip
        mod_zip = argv[1]

        find_mod_folder()
        unzip_mod_zip()
        modify_dot_mod()
        quit()

    except IndexError:
        find_mod_folder()
        open_path()
