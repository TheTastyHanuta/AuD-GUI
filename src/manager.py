import logging
from typing import List
import os
import shutil
import datetime
import subprocess
import platform
import pandas as pd
import csv
from tkinter import filedialog
from tkinter import messagebox

from src.comment_utils import State, Settings
from src.io_utils import copy_import_data, check_updates, copy_import_src

# Configure Log
logging.basicConfig(
    level=logging.DEBUG,
    filename=f"logs/{str(datetime.date.today())}_AuDGUI.log",
    filemode="a",
    format="{asctime} - {levelname} - {message}",
    style="{",
    datefmt="%Y-%m-%d %H:%M"
)


class Manager:
    def __init__(self, path_of_mainfile: str):
        logging.debug("manager.py: Start of GUI and creation of manager")
        # Path variables
        self.path = path_of_mainfile
        self.path_to_templates = os.path.join(self.path, "templates")
        self.path_to_data = os.path.join(self.path, "data")
        self.path_to_settings = os.path.join(self.path, "settings")
        self.path_to_output = os.path.join(self.path, "out")
        self.path_to_tmp = os.path.join(self.path, ".tmp")
        # Late initialization
        self.code_dir = ""
        self.pdf_dir = ""
        self.path_to_status_csv = ""
        self.dir_name = ""

        # Settings
        if "settings.json" in os.listdir(self.path_to_settings):
            # Load from JSON file
            self.settings = Settings(json_file=os.path.join(self.path_to_settings, "settings.json"))
        else:
            # Create new settings from scratch
            self.settings = Settings(personal_annotation="Korrigiert von Friedrich-Alexander\n"
                                                         "Bitte Korrektur-PDF beachten :)\n"
                                                         "(E-mail: friedrich.alexander@fau.de)",
                                     filepath=self.path_to_settings)
            self.settings.save()

        # Important state variables
        self.team_idx: int = 0  # Current index of team in team_list
        self.team_state: State = None
        self.team_list: list = []  # List of all team ids (or names?)
        self.states: List[State] = []  # List of all team states (State objects)

    def import_data(self, res):
        logging.debug("manager.py: import_data")
        filename, template, team_ids = res

        # copy_import_src(self.path_to_tmp, filename, self.path_to_data)
        # return

        # dir_name = copy_import_data(filename, self.path_to_data)
        dir_name = copy_import_src(self.path_to_tmp, filename, self.path_to_data)
        if dir_name is None:
            logging.debug("import_data: Import folder is not valid or does not exist")
            return
        self.team_list = team_ids
        self.dir_name = os.path.split(dir_name)[-1]  # Store for later usage

        logging.debug(f"import_data: Importing to \"{dir_name}\"")
        # Convert content of dir_name to comments
        template_file = [t for t in os.listdir(self.path_to_templates) if template in t][0]
        logging.debug(f"import_data: Using template \"{template}\" ({template_file})")

        logging.debug(f"import_data: Path info:\n"
                      f"self.path: {self.path}\n"
                      f"dir_name: {dir_name}\n"
                      f"Joined: {os.path.join(self.path, dir_name)}\n"
                      f"Content: {os.listdir(os.path.join(self.path, dir_name))}")

        self.code_dir = os.path.join(self.path,
                                     dir_name,
                                     [i for i in os.listdir(os.path.join(self.path, dir_name)) if
                                      "Code" in i and os.path.isdir(os.path.join(self.path, dir_name, i))][0],
                                     "Abgaben")
        self.pdf_dir = os.path.join(self.path,
                                    dir_name,
                                    [i for i in os.listdir(os.path.join(self.path, dir_name)) if
                                     "Korrektur" in i and os.path.isdir(os.path.join(self.path, dir_name, i))][0],
                                    "Abgaben")
        logging.debug(f"Path info:\nCode: {self.code_dir}\nPDFs: {self.pdf_dir}")
        # Remove files that are not necessary
        # List of teams to keep
        team_folders_to_keep = ["Team " + i for i in team_ids]
        logging.debug(f"import_data: Keep teams {team_folders_to_keep}")

        # Remove from code_dir and status.csv
        for f in os.listdir(self.code_dir):
            if f not in team_folders_to_keep:
                f_to_remove = os.path.join(self.code_dir, f)
                if os.path.isdir(f_to_remove):
                    shutil.rmtree(f_to_remove)
                elif os.path.isfile(f_to_remove):
                    os.remove(f_to_remove)

        # Remove from pdf_dir but keep status.csv
        for f in os.listdir(self.pdf_dir):
            if f not in team_folders_to_keep and f != "status.csv":
                f_to_remove = os.path.join(self.pdf_dir, f)
                if os.path.isdir(f_to_remove):
                    shutil.rmtree(f_to_remove)
            elif f == "status.csv":
                self.path_to_status_csv = os.path.join(self.pdf_dir, f)

        self.states = [State(team_id=i,
                             template_file=os.path.join(self.path_to_templates, template_file),
                             code_dir=self.code_dir,
                             pdf_dir=self.pdf_dir,
                             status_file=self.path_to_status_csv) for i in team_ids]

        # Check if all teams were found
        check_ids = [str(i.id) for i in self.states]
        if not check_ids == self.team_list:
            missing_teams = [t for t in self.team_list if t not in check_ids]
            messagebox.showerror(title="AuD-GUI :D - Fehler!",
                                 message=f"IDs {', '.join(missing_teams)} fehlen!"
                                         f"Es werden nur die existierenden Teams importiert.")
            logging.error(f"import_data: Teams {missing_teams} missing. Importing only {check_ids}.")
            self.team_list = check_ids

    def open_data(self):
        logging.debug("manager.py: open_data")
        chosen_directory = filedialog.askdirectory(initialdir=self.path_to_data)

        if chosen_directory:
            logging.debug(f"open_data: Open directory \"{chosen_directory}\"")
            try:
                self.code_dir = os.path.join(chosen_directory,
                                             [i for i in os.listdir(chosen_directory) if
                                              "Code" in i and os.path.isdir(os.path.join(chosen_directory, i))][0],
                                             "Abgaben")
                self.pdf_dir = os.path.join(chosen_directory,
                                            [i for i in os.listdir(chosen_directory) if
                                             "Korrektur" in i and os.path.isdir(os.path.join(chosen_directory, i))][0],
                                            "Abgaben")
                self.dir_name = os.path.split(chosen_directory)[-1]
            except OSError:
                logging.exception("open_data: Directory not found")
            except IndexError:
                logging.exception("open_data: Directory is missing")

            try:
                files = []
                for team in os.listdir(self.pdf_dir):
                    if os.path.isdir(os.path.join(self.pdf_dir, team)):
                        for file in os.listdir(os.path.join(self.pdf_dir, team)):
                            if file == "state.json":
                                files.append(os.path.join(self.pdf_dir, team, file))
                self.states = [State(json_file=f) for f in files]
                self.team_list = [str(s.id) for s in self.states]
                logging.debug(f"open_data: Teams {self.team_list} loaded.")
                if len(self.states) == 0:
                    logging.exception(f"open_data: No states found in {self.pdf_dir}")
            except OSError:
                logging.exception("open_data: OSError while searching for states")

            return True
        else:
            logging.debug("open_data aborted by user")
            return False

    def open_team(self, index: int):
        logging.debug("manager.py: open_team")
        logging.debug(f"open_team: Open team at index {index}")
        self.team_idx = index
        self.team_state = self.states[self.team_idx]
        logging.debug(f"open_team: Open team {self.team_state.id}")

    def open_pdf(self):
        logging.debug("manager.py: open_pdf")
        logging.debug(f"open_pdf: Open PDF for team {self.team_state.id} (Location: \"{self.team_state.pdf}\")")
        # Nice extra functionality to reduce pain while correcting ;)
        if platform.system() == "Darwin":
            subprocess.Popen(["open", self.team_state.pdf])
        else:
            subprocess.Popen([self.team_state.pdf], shell=True)

    def save(self):
        logging.debug("manager.py: save")
        for i in self.states:
            i.save()
        logging.debug("save: Saved successfully")

    # Main frame functions
    def get_id(self):
        return self.team_state.id

    def get_confirmed(self):
        return self.team_state.confirmed

    def switch_confirmed(self):
        logging.debug("manager.py: switch_confirmed")
        self.team_state.confirmed = not self.team_state.confirmed
        logging.debug(f"switch_confirmed: Team {self.team_state.id}: {self.team_state.confirmed}")

    def get_total_points(self):
        """
        :return: Total points in format {"actual": ..., "max": ...}
        """
        return self.team_state.comment["total_points"]

    def get_class_points(self, class_str):
        return self.team_state.comment["classes"][self.get_class_idx(class_str)]["points"]

    def get_task_points(self, class_str, task_str):
        return self.team_state.comment["classes"][self.get_class_idx(class_str)]["tasks"][
            self.get_task_idx(class_str, task_str)]["points"]

    def get_compile_error(self):
        return self.team_state.comment["compile_error"]

    def switch_compile_error(self):
        logging.debug("manager.py: switch_compile_error")
        self.team_state.comment["compile_error"] = not self.team_state.comment["compile_error"]
        logging.debug(f"switch_compile_error: Team {self.team_state.id}: {self.team_state.comment['compile_error']}")

    def get_class_idx(self, class_str):
        for idx, i in enumerate(self.team_state.comment["classes"]):
            if i["title"] == class_str:
                return idx
        logging.error(f"Class \"{class_str}\" does not exist in current status file")
        return None

    def get_task_idx(self, class_str, task_str):
        class_idx = self.get_class_idx(class_str)
        if class_idx is not None:
            for idx, i in enumerate(self.team_state.comment["classes"][class_idx]["tasks"]):
                if i["title"] == task_str:
                    return idx
            logging.error(f"Class \"{class_str}\" has no task \"{task_str}\"!")
        return None

    def update_total_points(self):
        total_sum = 0.
        if not self.team_state.comment["compile_error"]:
            for i, c in enumerate(self.team_state.comment["classes"]):
                self.update_class_points(c["title"])
                total_sum += self.team_state.comment["classes"][i]["points"]["actual"]
        self.team_state.comment["total_points"]["actual"] = min(total_sum,
                                                                self.team_state.comment["total_points"]["max"])

    def update_class_points(self, class_str: str):
        summed_points = 0.
        idx = self.get_class_idx(class_str)
        if idx is None:
            return
        for t in self.team_state.comment["classes"][idx]["tasks"]:
            summed_points += t["points"]["actual"]
        self.team_state.comment["classes"][idx]["points"]["actual"] = summed_points

    def increase_task_points(self, class_str: str, task_str: str):
        """
        Retrieves indices defined by class and task name and increases the points of that specific task by 0.5.
        Higher points than the max points are not possible.

        :param class_str: Title of the class
        :param task_str: Title of the task
        """
        class_idx = self.get_class_idx(class_str)
        if class_idx is not None:
            task_idx = self.get_task_idx(class_str, task_str)
            if task_idx is not None:
                self.team_state.comment["classes"][class_idx]["tasks"][task_idx]["points"]["actual"] = min(
                    self.team_state.comment["classes"][class_idx]["tasks"][task_idx]["points"]["actual"] + 0.5,
                    self.team_state.comment["classes"][class_idx]["tasks"][task_idx]["points"]["max"]
                )
                # Update total points after updating task points
                self.update_total_points()

    def decrease_task_points(self, class_str: str, task_str: str):
        """
        Retrieves indices defined by class and task name and decreases the points of that specific task by 0.5.
        Lower points than 0 points are not possible.

        :param class_str: Title of the class
        :param task_str: Title of the task
        """
        class_idx = self.get_class_idx(class_str)
        if class_idx is not None:
            task_idx = self.get_task_idx(class_str, task_str)
            if task_idx is not None:
                self.team_state.comment["classes"][class_idx]["tasks"][task_idx]["points"]["actual"] = max(
                    self.team_state.comment["classes"][class_idx]["tasks"][task_idx]["points"]["actual"] - 0.5,
                    0.
                )
                # Update total points after updating task points
                self.update_total_points()

    def save_personal_comment(self, comment: str):
        logging.debug("manager.py: save_personal_comment")
        self.settings.personal_annotation = comment.rstrip("\n")  # Remove trailing newlines
        self.settings.save()
        logging.debug(f"save_personal_comment: Saved \"{self.settings.personal_annotation}\"")

    def export(self, zip_name: str):
        logging.debug("manager.py: export")
        if zip_name == "":
            messagebox.showerror(title="AuD-GUI :D - Fehler!",
                                 message="Name des Export-Ordners darf nicht leer sein!")
            logging.error("export: Zip-folder name empty")
            return
        res = []
        for s in self.states:
            points, feedback = s.export()
            feedback += f"\n{self.settings.personal_annotation}"
            res.append((str(s.id), points, feedback))  # Add ID, total points, comment feedback
        logging.debug("export: Created export list successfully")

        export_path = os.path.join(self.path_to_output, self.dir_name, zip_name, zip_name)
        logging.debug(f"Try to export to \"{export_path}\"")

        # Check if directory already exist
        if os.path.isdir(export_path):
            logging.debug(f"export: Directory \"{export_path}\" already exists")
            # Ask for permission to delete it
            remove_dir = messagebox.askokcancel(title="AuD-GUI :D - Warnung!",
                                                message=f"Ordner {export_path} existiert bereits. "
                                                        f"Ordner durch neuen Inhalt ersetzen? "
                                                        f"(Bisheriger Inhalt wird gelöscht!)")
            if remove_dir:
                logging.debug(f"export: Permission given -> remove directory \"{export_path}\"")
                shutil.rmtree(export_path)
            else:
                # Cancel operation if ordner deletion is not performed
                logging.debug("export: Permission not given -> abort")
                return

        shutil.copytree(src=self.pdf_dir, dst=export_path)
        logging.debug(f"export: Copy folder \"{self.pdf_dir}\" to \"{export_path}\"")

        path_to_status_csv = os.path.join(export_path, "status.csv")
        try:
            logging.debug(f"export: Try to open \"{path_to_status_csv}\"")
            with open(path_to_status_csv, encoding="utf-8", errors="backslashreplace") as input_fd:
                status_df = pd.read_csv(input_fd)
        except OSError:
            messagebox.showerror(title="AuD-GUI :D - Fehler!", message="status.csv existiert nicht!")
            logging.exception("export: status.csv not found")
            return

        # Find column with ID (Could be team_id or usr_id)
        id_col = [i for i in status_df.keys() if "id" in i][0]

        # Cast column values to correct dtype
        status_df["mark"] = status_df["mark"].astype(float)
        status_df[id_col] = status_df[id_col].astype(str)

        for team_id, team_points, team_comment in res:

            # Remove all files that are not "Korrektur.pdf"
            team_folder = [t for t in os.listdir(export_path) if team_id in t][0]
            for file in os.listdir(os.path.join(export_path, team_folder)):
                if file != "Korrektur.pdf":
                    os.remove(os.path.join(export_path, team_folder, file))
                    logging.debug(f"export: Remove \"{os.path.join(export_path, team_folder, file)}\"")

            # Set score
            status_df.loc[status_df[id_col] == team_id, "mark"] = team_points
            # Set comment
            status_df.loc[status_df[id_col] == team_id, "comment"] = team_comment
            # Set update column to 1
            status_df.loc[status_df[id_col] == team_id, "update"] = 1

        # Check if all updates were done
        if not check_updates(status_df, self.team_list):
            messagebox.showerror(title="AuD-GUI :D - Fehler!",
                                 message="Die Anzahl an Updates stimmt nicht überein!")
            logging.error("export: Number of updates in status.csv is not correct")
            return

        # export status.csv
        status_df.to_csv(path_to_status_csv, index=False, quoting=csv.QUOTE_ALL, float_format="%g")

        shutil.make_archive(base_name=os.path.join(self.path_to_output, self.dir_name, zip_name),  # Destination
                            format="zip",  # Extension
                            root_dir=os.path.join(self.path_to_output, self.dir_name, zip_name))  # Folder to zip
        logging.debug(f"export: Converted to zip file "
                      f"\"{os.path.join(self.path_to_output, self.dir_name, zip_name)}.zip\"")
        open_folder = messagebox.askyesno(title="AuD-GUI :D - Export",
                                          message=f"Datei \""
                                                  f"{os.path.join(self.path_to_output, self.dir_name, zip_name)}.zip"
                                                  f"\" anzeigen?")
        if open_folder:
            os.startfile(os.path.join(self.path_to_output, self.dir_name))
            logging.debug(f"export: Open in file explorer: "
                          f"\"{os.path.join(self.path_to_output, self.dir_name, zip_name)}.zip\"")
