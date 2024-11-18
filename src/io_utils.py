import os
import datetime
import shutil
from tkinter import messagebox


def extract_zip_to_tmp(path_to_tmp: str, zip_path: str):
    if os.path.isfile(zip_path) and zip_path.endswith(".zip"):
        src = zip_path
        dst = os.path.join(path_to_tmp, "tmp_copy")
        shutil.unpack_archive(filename=src, extract_dir=dst, format="zip")
    else:
        dst = ""
    return dst


def copy_import_src(path_to_tmp: str, chosen_path: str, path_to_data: str):
    search_dir = ""
    if os.path.isfile(chosen_path) and chosen_path.endswith(".zip"):
        search_dir = extract_zip_to_tmp(path_to_tmp, chosen_path)
    elif os.path.isdir(chosen_path):
        search_dir = chosen_path
    else:
        print("Error: File but no ZIP")

    if not search_dir:
        return

    content_src = ""
    for dirpath, dirnames, _ in os.walk(search_dir):
        code = [i for i in dirnames if "Code" in i]
        pdf = [i for i in dirnames if "Korrektur" in i]

        if len(code) > 0 and len(pdf) > 0:
            content_src = dirpath
            break

    name = str(datetime.date.today()) + "_" + os.path.splitext(os.path.split(chosen_path)[-1])[0]
    content_dst = os.path.join(path_to_data, name)

    if os.path.isdir(content_dst):
        replace = messagebox.askokcancel(title="AuD-GUI :D - Warnung!",
                                         message=f"Ordner \"{content_dst}\" existiert bereits.\n"
                                                 f"Trotzdem fortfahren und den bisherigen Ordner überschreiben?")
        if replace:
            # no permission to replace existing folder => terminate
            shutil.rmtree(content_dst)
        else:
            return None

    shutil.copytree(src=content_src, dst=content_dst)

    clear_tmp(path_to_tmp)
    return content_dst


def clear_tmp(path_to_tmp: str):
    if os.path.isdir(path_to_tmp) and path_to_tmp.endswith(".tmp"):
        for d in os.listdir(path_to_tmp):
            if d != ".gitkeep":
                shutil.rmtree(os.path.join(path_to_tmp, d))


def copy_import_data(filename: str, path_to_data: str):
    """
    Copies the content of the folder.

    :param filename: filename of a .zip-file
    :param path_to_data: Path to the data storage folder
    """
    if not ((os.path.isfile(filename) and filename.endswith(".zip")) or (os.path.isdir(filename))):
        # TODO: Log ???
        return
    f = os.path.split(filename)[-1]  # Extract real filename without directory
    f = os.path.splitext(f)[0]
    dir_name = os.path.join(path_to_data, str(datetime.date.today()) + "_" + f)
    if os.path.isdir(dir_name):
        replace = messagebox.askokcancel(title="AuD-GUI :D - Warnung!",
                                         message=f"Ordner \"{dir_name}\" existiert bereits.\n"
                                                 f"Trotzdem fortfahren und den bisherigen Ordner überschreiben?")
        if not replace:
            # no permission to replace existing folder => terminate
            return
    if os.path.isfile(filename) and filename.endswith(".zip"):
        shutil.unpack_archive(filename, dir_name)
        return dir_name
    elif os.path.isdir(filename):
        # TODO: Import from folder (Copy folder instead of extracting it) => shutil.copytree(...)
        return


# Function to check number of updates
def check_updates(dataframe, id_list):
    updates = [entry for entry in dataframe["update"] if entry == 1]
    return len(updates) == len(id_list)
