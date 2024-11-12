import os
import datetime
import shutil
from tkinter import messagebox


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
        # TODO: Import from folder (Copy folder instead of extracting it)
        return


# Function to check number of updates
def check_updates(dataframe, id_list):
    updates = [entry for entry in dataframe["update"] if entry == 1]
    return len(updates) == len(id_list)
