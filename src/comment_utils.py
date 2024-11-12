import os
import shutil
import json
import pandas as pd
from tkinter import messagebox


class Settings:
    def __init__(self, personal_annotation: str = "", filepath: str = "", json_file: str = ""):
        if json_file != "":
            # Initialization via json dict
            with open(json_file, "r", encoding="utf-8") as f:
                json_data = json.load(f)
                self.__dict__.update(json_data)
        else:
            self.settings_path = os.path.join(filepath, "settings.json")
            self.personal_annotation = personal_annotation

    def save(self):
        """
        Saves the settings as JSON file at the location stored in settings_path
        """
        with open(self.settings_path, "w", encoding="utf-8") as f:
            json.dump(self.__dict__, f, indent=4, ensure_ascii=False)


class State:
    def __init__(self, team_id: str = "",
                 template_file: str = "",
                 code_dir: str = "",
                 pdf_dir: str = "",
                 status_file: str = "",
                 json_file: str = ""):
        if json_file != "":
            # Initialization via json dict
            with open(json_file, "r", encoding="utf-8") as f:
                json_data = json.load(f)
                self.__dict__.update(json_data)
        else:
            # New instance
            self.id = int(team_id)
            self.confirmed = False

            # Define directories
            code_dir = os.path.join(code_dir, "Team " + str(self.id))
            pdf_dir = os.path.join(pdf_dir, "Team " + str(self.id))

            # Code files
            self.code = [os.path.join(code_dir, i) for i in os.listdir(code_dir)]

            # Remove other files and define Korrektur-file
            for i in os.listdir(pdf_dir):
                if i == "Korrektur.pdf":
                    self.pdf = os.path.join(pdf_dir, i)
                else:
                    os.remove(os.path.join(pdf_dir, i))

            self.status_filepath = os.path.join(pdf_dir, "state.json")
            # Copy template file
            shutil.copyfile(src=template_file, dst=self.status_filepath)

            self.status_csv = status_file

            # Extract template
            with open(self.status_filepath, "r", encoding="utf-8") as f:
                d = json.load(f)

            # Define comment
            self.comment = d

            # Try to load status.csv
            try:
                with open(self.status_csv, encoding="utf-8", errors="backslashreplace") as input_fd:
                    status_df = pd.read_csv(input_fd)
            except OSError:
                messagebox.showerror(title="AuD-GUI :D - Fehler!",
                                     message=f"status.csv liegt nicht unter dem Pfad \"{self.status_csv}\"!")
                return

            # Find column with ID (Could be team_id or usr_id)
            try:
                id_col = [i for i in status_df.keys() if "id" in i][0]
            except IndexError:
                messagebox.showerror(title="AuD-GUI :D - Fehler!",
                                     message="Keine Spalte für Team-IDs in \"status.csv\" gefunden!")
                return
            status_df[id_col] = status_df[id_col].astype(str)
            status_df["comment"] = status_df["comment"].fillna(value="")

            # Find row in dataframe and grab comment column value
            try:
                comment = status_df.loc[status_df[id_col] == str(self.id), "comment"].item()
            except ValueError:
                messagebox.showerror(title="AuD-GUI :D - Fehler!",
                                     message=f"Team {self.id} nicht in \"status.csv\" gefunden!")
                return

            # Grab current score
            score = status_df.loc[status_df[id_col] == str(self.id), "mark"].item()
            if pd.isna(score):
                score_string = "Punktzahl: \n"
            else:
                score_string = "Punktzahl: " + str(score) + "\n"

            # Make score string first line of comment file
            comment = score_string + comment

            self.auto_correction_result = comment

            # Save as json
            self.save()

    def save(self):
        """
        Saves the state as JSON file at the location stored in status_filepath
        """
        with open(self.status_filepath, "w", encoding="utf-8") as f:
            json.dump(self.__dict__, f, indent=4, ensure_ascii=False)

    def export(self):
        total = float(self.comment["total_points"]["actual"])

        res = f"Gesamt: {self.comment['total_points']['actual']} von {self.comment['total_points']['max']} Punkten\n"

        if self.comment["compile_error"]:
            res += "\nCompile-Error :(\n"
        else:
            for i, c in enumerate(self.comment["classes"]):
                res += f"\n{c['title']} ({c['points']['actual']} / {c['points']['max']}):\n"
                for t in self.comment["classes"][i]["tasks"]:
                    mark = "~"
                    if t["points"]["actual"] == t["points"]["max"]:
                        mark = "✓"
                    elif t["points"]["actual"] == 0.0:
                        mark = "✗"
                    res += f"{mark}   {t['points']['actual']} / {t['points']['actual']}  |  {t['title']}\n"

        return total, res
