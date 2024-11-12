import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import os


class ImportDialog(tk.Toplevel):
    def __init__(self,
                 master,
                 # size: tuple,
                 path_to_templates: str,
                 import_func):
        super().__init__(master=master)
        self.title("AuD-GUI :D - Abgaben importieren")
        self.resizable(False, False)
        self.focus_set()
        self.grab_set()

        # Read templates
        self.templates = [os.path.splitext(t)[0] for t in os.listdir(path_to_templates)]

        # STATES
        self.import_folder = tk.StringVar(value="")
        self.template_title = tk.StringVar(value="")
        self.team_ids = tk.StringVar(value="")
        self.import_func = import_func

        # WIDGETS

        # Input label
        self.input_label = tk.Label(self, text="Ordner auswählen:")
        self.input_label.pack(padx=10, pady=5, anchor="w")

        # Folder entry field
        self.entry_frame = tk.Frame(self)
        self.input_entry = tk.Entry(self.entry_frame, width=50, textvariable=self.import_folder)
        self.input_entry.pack(anchor="w", side="left", fill="x", expand=True)

        # Search button
        self.search_button = tk.Button(self.entry_frame, text="Durchsuchen", command=self.search_folder)
        self.search_button.pack(padx=10, side="right", anchor="e")
        self.entry_frame.pack(padx=10, pady=5, anchor="w", fill="x", expand=True)

        # Template label
        self.template_label = tk.Label(self, text="Template auswählen:")
        self.template_label.pack(padx=10, pady=5, anchor="w")

        # Template choose box
        self.template_box = ttk.Combobox(self,
                                         state="readonly",
                                         values=self.templates,
                                         textvariable=self.template_title)
        self.template_box.pack(padx=10, pady=5, anchor="w")

        # Team-ID label
        self.id_label = tk.Label(self, text="Team-IDs eingeben:")
        self.id_label.pack(padx=10, pady=5, anchor="w")

        # Team-ID box
        self.id_box = tk.Text(self, width=20, height=10)
        self.id_box.pack(padx=10, pady=5, anchor="w")

        # Termination frame
        self.terminate_frame = tk.Frame(self)

        # Abort button
        self.abort_button = tk.Button(self.terminate_frame, text="Abbrechen", command=self.abort)
        self.abort_button.pack(padx=10, pady=5, anchor="e", side="right")

        # Import button
        self.import_button = tk.Button(self.terminate_frame, text="Importieren", command=self.import_data)
        self.import_button.pack(padx=10, pady=5, anchor="e", side="right")

        self.terminate_frame.pack(padx=10, pady=5, anchor="w", fill="x")

    def search_folder(self):
        # TODO: Allow folders
        self.import_folder.set(filedialog.askopenfilename(parent=self, filetypes=[("ZIP Files", "*.zip")]))

    def import_data(self):
        # Set text widget to variable
        self.team_ids.set(self.id_box.get("1.0", "end"))
        res = [self.import_folder.get(),
               self.template_title.get(),
               [i for i in self.team_ids.get().splitlines() if i != ""]]
        self.destroy()
        self.import_func(res)

    def abort(self):
        # Set all entries to empty
        self.import_folder.set("")
        self.template_title.set("")
        self.team_ids.set("")

        self.destroy()


class SettingsDialog(tk.Toplevel):
    def __init__(self,
                 master,
                 name: str,
                 save_func):
        super().__init__(master=master)  # , width=size[0], height=size[1]
        # self.geometry(f"{size[0]}x{size[1]}+100+100")
        self.title("AuD-GUI :D - Einstellungen")
        self.resizable(False, False)
        self.focus_set()
        self.grab_set()

        # STATES
        self.name = name
        self.save_func = save_func

        # WIDGETS

        # Input label
        self.input_label = tk.Label(self, text="Persönlicher Kommentar:", anchor="w")
        self.input_label.pack(fill="x", side="top", anchor="w", padx=10, pady=5)

        # String box
        self.id_box = tk.Text(self, width=50, height=10)
        self.id_box.insert(tk.END, self.name)
        self.id_box.pack(fill="x", side="top", anchor="w", padx=10, pady=5)

        self.info_label = ttk.Label(self, text="INFO:\nDieser Kommentar wird unter jedem Comment angefügt.", anchor="w")
        self.info_label.pack(fill="x", side="top", anchor="w", padx=10, pady=5)

        # Termination frame
        self.terminate_frame = tk.Frame(self)

        # Abort button
        self.abort_button = tk.Button(self.terminate_frame, text="Abbrechen", command=self.abort)
        self.abort_button.pack(padx=10, pady=5, anchor="e", side="right")

        # Import button
        self.import_button = tk.Button(self.terminate_frame, text="Speichern", command=self.accept)
        self.import_button.pack(padx=10, pady=5, anchor="e", side="right")

        self.terminate_frame.pack(padx=10, pady=5, anchor="w", fill="x")

    def accept(self):
        name = self.id_box.get("1.0", "end")
        self.destroy()
        self.save_func(name)

    def abort(self):
        self.destroy()


class ExportDialog(tk.Toplevel):
    def __init__(self,
                 master,
                 export_func):
        super().__init__(master=master)
        self.title("AuD-GUI :D - Korrektur exportieren")
        self.resizable(False, False)
        self.focus_set()
        self.grab_set()

        # STATES
        self.export_folder = tk.StringVar(value="")
        self.export_func = export_func

        # WIDGETS

        # Input label
        self.input_label = tk.Label(self, text="Exportieren als:")
        self.input_label.pack(padx=10, pady=5, anchor="w", side="top")

        # Folder entry field
        self.input_entry = tk.Entry(self, width=50, textvariable=self.export_folder)
        self.input_entry.pack(anchor="w", side="top", fill="x", expand=True, padx=10)

        # Info label
        self.info_label = tk.Label(self,
                                   text="INFO:\nUm die Korrektur in StudOn hochladen zu können, "
                                        "benötigt der Ordner einen speziellen Namen.\nDieser kann auf StudOn "
                                        "heruntergeladen werden und hier eingefügt werden.",
                                   justify="left",
                                   anchor="w")
        self.info_label.pack(padx=10, pady=5, anchor="w")

        # Termination frame
        self.terminate_frame = tk.Frame(self)

        # Abort button
        self.abort_button = tk.Button(self.terminate_frame, text="Abbrechen", command=self.abort)
        self.abort_button.pack(padx=10, pady=5, anchor="e", side="right")

        # Import button
        self.export_button = tk.Button(self.terminate_frame, text="Exportieren", command=self.export_data)
        self.export_button.pack(padx=10, pady=5, anchor="e", side="right")

        self.terminate_frame.pack(padx=10, pady=5, anchor="w", fill="x")

    def export_data(self):
        self.destroy()
        self.export_func(self.export_folder.get())

    def abort(self):
        self.destroy()
