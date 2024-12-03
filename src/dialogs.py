import tkinter as tk
from tkinter import ttk
import os
from tkinter import filedialog, simpledialog, messagebox
import json
from typing import Union


class ImportDialog(tk.Toplevel):
    def __init__(self,
                 master,
                 allow_folders: bool,
                 path_to_templates: str,
                 import_func):
        super().__init__(master=master)
        self.title("AuD-GUI :D - Abgaben importieren")
        self.resizable(False, False)
        self.focus_set()
        self.grab_set()
        self.allow_folders = allow_folders

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
        if self.allow_folders:
            self.import_folder.set(filedialog.askdirectory(parent=self))
        else:
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


class Category:
    def __init__(self, title: str):
        self.title = title
        self.annotations = []

    def add_annotation(self, annotation: str):
        self.annotations.append(annotation)

    def delete_annotation(self, annotation: Union[int, str]):
        try:
            if type(annotation) == int:
                self.annotations.remove(self.annotations[annotation])
            elif type(annotation) == str:
                self.annotations.remove(annotation)
        except ValueError:
            print(f"Annotation \"{annotation}\" not in Category \"{self.title}\"")

    def get_num_annotations(self) -> int:
        return len(self.annotations)

    def __eq__(self, other):
        if isinstance(other, Category):
            return self.title == other.title
        else:
            return False


class ClipboardApp(tk.Toplevel):
    def __init__(self, master, path_to_data: str):
        super().__init__(master=master)
        self.title("AuD-GUI :D - Korrekturhilfe")
        self.geometry("600x600")

        # Variables
        self.data: list[Category] = []
        self.selected_category = -1
        self.path_to_data_file = path_to_data

        self.protocol("WM_DELETE_WINDOW", self.close)

        # Widgets
        # Sidebar
        self.sidebar_buttons: list[tk.Button] = []
        self.sidebar_frames: list[tk.Frame] = []

        self.sidebar_frame = tk.Frame(self, highlightbackground="gray", highlightthickness=2)

        self.sidebar_title_frame = tk.Frame(self.sidebar_frame)
        self.sidebar_title = tk.Label(self.sidebar_title_frame,
                                      text="Kategorie",
                                      width=10,
                                      bg="gray",
                                      font=("Arial", 18),
                                      relief="solid")
        self.sidebar_title.pack(fill="x",
                                expand=True,
                                side="top",
                                anchor="n")
        # Buttons
        self.sidebar_button_frame = tk.Frame(self.sidebar_title_frame)
        self.plus_button = tk.Button(self.sidebar_button_frame, text="+", font=("Arial", 16),
                                     command=self.add_category)
        self.plus_button.pack(fill="x", side="left", anchor="n", expand=True)
        self.minus_button = tk.Button(self.sidebar_button_frame, text="-", font=("Arial", 16),
                                      command=self.delete_category)
        self.minus_button.pack(fill="x", side="right", anchor="n", expand=True)
        self.sidebar_button_frame.pack(fill="x", side="top", anchor="n", expand=True)

        self.sidebar_title_frame.pack(fill="x", side="top", anchor="n")

        self.update_sidebar()

        self.sidebar_frame.pack(fill="both",
                                side="left",
                                anchor="nw")

        # Main frame
        self.main_frames = []

        self.main_frame = tk.Frame(self, highlightbackground="gray", highlightthickness=2)

        self.main_title_frame = tk.Frame(self.main_frame)
        self.main_title = tk.Label(self.main_title_frame,
                                   text="Anmerkungen",
                                   bg="gray",
                                   font=("Arial", 18),
                                   relief="solid")
        self.main_title.pack(fill="x",
                             expand=True,
                             side="top",
                             anchor="n")

        self.main_title_frame.pack(fill="x", side="top", anchor="n")

        self.add_button = tk.Button(self.main_frame, text="+", font=("Arial", 16), command=self.add_annotation)
        self.add_button.pack(fill="x")

        self.update_main_frame()

        self.main_frame.pack(fill="both",
                             side="right",
                             anchor="ne",
                             expand=True)

        # Load stored data
        self.load()

    def update_sidebar(self):
        # Forget old content
        for f in self.sidebar_frames:
            f.pack_forget()
        self.sidebar_frames.clear()

        # Create new content
        for i, c in enumerate(self.data):
            f = tk.Frame(self.sidebar_frame, highlightbackground="gray", highlightthickness=5)
            b = tk.Button(f, text=c.title, command=lambda x=i: self.open_category(x))
            b.pack(fill="x")
            f.pack(fill="x", padx=2, pady=2, side="top", anchor="n")
            self.sidebar_frames.append(f)
            self.sidebar_buttons.append(b)
        self.color_sidebar()

    def color_sidebar(self):
        for i in range(len(self.sidebar_frames)):
            if i == self.selected_category:
                self.sidebar_frames[i].configure(highlightbackground="blue")
            else:
                self.sidebar_frames[i].configure(highlightbackground="gray")

    def open_category(self, index: int):
        self.selected_category = index
        self.color_sidebar()
        self.update_main_frame()

    def add_category(self):
        title = simpledialog.askstring(title="Kategorie hinzufügen", prompt="Bezeichung:\t\t\t", parent=self)
        if title is not None:
            c = Category(title)
            if c in self.data:
                messagebox.showerror(title="Fehler", message=f"Kategorie \"{c.title}\" existiert bereits!", parent=self)
                return
            self.data.append(c)
            self.update_sidebar()

    def delete_category(self):
        if self.selected_category >= 0:
            permission = messagebox.askyesno(title="Kategorie entfernen",
                                             message=f"Kategorie \"{self.data[self.selected_category].title}\" "
                                                     f"unwiderruflich löschen?",
                                             parent=self)
            if permission:
                self.data.remove(self.data[self.selected_category])
                self.selected_category = -1
                self.update_sidebar()
                self.update_main_frame()

    def update_main_frame(self):
        if len(self.main_frames) > 0:
            for f in self.main_frames:
                f.pack_forget()
            self.main_frames.clear()

        if self.selected_category >= 0:
            for an in self.data[self.selected_category].annotations:
                f = tk.Frame(self.main_frame)
                b0 = tk.Button(f, text="-", width=10,
                               command=lambda x=an: self.delete_annotation(x))
                text = tk.Label(f, text=an)
                b1 = tk.Button(f, text="Copy", width=10,
                               command=lambda x=an: self.copy_to_clipboard(x))
                b0.pack(side="left")
                text.pack(side="left")
                b1.pack(side="right")
                f.pack(fill="x", anchor="w", side="top")
                self.main_frames.append(f)

    def add_annotation(self):
        if self.selected_category >= 0:
            annotation = simpledialog.askstring(title="Anmerkung hinzufügen", prompt="Text:" + "\t" * 10, parent=self)
            if annotation is not None:
                self.data[self.selected_category].add_annotation(annotation)
                self.update_main_frame()

    def delete_annotation(self, x: str):
        if self.selected_category >= 0:
            self.data[self.selected_category].delete_annotation(x)
            self.update_main_frame()

    def copy_to_clipboard(self, content: str):
        self.clipboard_clear()
        self.clipboard_append(content)

        self.update()

    def save(self):
        save_data = []
        for c in self.data:
            save_data.append({"title": c.title, "annotations": c.annotations})

        # Write the data to a JSON file
        with open(os.path.join(self.path_to_data_file), "w", encoding="utf-8") as f:
            json.dump(save_data, f, indent=4, ensure_ascii=False)  # indent=4 is optional but makes it pretty-printed

    def load(self):
        if os.path.isfile(self.path_to_data_file):
            with open(self.path_to_data_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            for d in data:
                c = Category(d["title"])
                for t in d["annotations"]:
                    c.add_annotation(t)
                self.data.append(c)
            self.update_sidebar()
            self.update_main_frame()

    def close(self):
        self.clipboard_clear()
        self.save()
        self.destroy()
