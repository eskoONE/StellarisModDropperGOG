from os import path, chdir, makedirs, listdir
from zipfile import ZipFile
import sys
from subprocess import Popen

# Stellaris mod folder path for the GOG version of the game
mod_path = "\\Documents\\Paradox Interactive\\Stellaris\\mod"
# expected full user mod path on Windows 10
usr_mod_path = path.expanduser("~") + mod_path
# onto the pyscript drag and dropped zip file

# test.zip path, this is obsolute
# mod_zip = os.path.expanduser("~") + "\\Downloads\\test_mod.zip"


def find_mod_folder():
    # change dir to mod folder if it exists, if not create it
    if path.exists(usr_mod_path):
        chdir(usr_mod_path)
        print(listdir())

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
    f = open(usr_mod_path + "\\" + dot_mod, "r+")

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


if __name__ == "__main__":
    input()

    global mod_zip
    mod_zip = sys.argv[1]

    if not mod_zip == sys.argv[1]:
        Popen('explorer "{0}"'.format(usr_mod_path))
        print("you are here")

    else:
        find_mod_folder()
        unzip_mod_zip()
        modify_dot_mod()
        quit()
