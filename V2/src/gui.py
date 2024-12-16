import tkinter as tk
from tkinter import messagebox, simpledialog
from tkinter import ttk
import os

from V2.src.gui_utils import Window, DoubleScrolledFrame
from V2.src.manager import Manager
from V2.src.graphics import Graphics
from V2.src.dialogs import ImportDialog, ExportDialog, SettingsDialog


class AuDGUI(Window):
    def __init__(self, start_path: str):
        super().__init__(title="AuD-GUI :D")
        self.main_path = start_path

        self.g = Graphics()

        self.manager = Manager(path_of_mainfile=self.main_path)

        self.active_left_frame = False
        self.active_right_frame = False
        self.active_progress_bar = False

        # Menu
        # File menu
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.file_menu.add_command(label="Korrektur öffnen", command=self.open_data)
        self.file_menu.add_separator()
        self.import_menu = tk.Menu(self.file_menu, tearoff=0)
        self.import_menu.add_command(label="Ordner", command=lambda: self.import_dialog(allow_folders=True))
        self.import_menu.add_command(label="Zip-Datei", command=lambda: self.import_dialog(allow_folders=False))
        self.file_menu.add_cascade(label="Abgaben importieren", menu=self.import_menu)
        self.file_menu.add_command(label="Korrekturen exportieren", command=self.export_data, state="disabled")
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Speichern", accelerator="Strg + S", command=self.save)
        self.bind_all("Strg + S", self.save)  # Bind accelerator
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Einstellungen", command=self.settings_dialog)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Beenden", command=self.close)

        # Check if there are already loaded corrections
        if len(os.listdir(self.manager.path_to_data)) == 0:
            self.file_menu.entryconfigure("Korrektur öffnen", state="disabled")

        # Add to main menu
        self.menu_bar.add_cascade(label="Datei", menu=self.file_menu)

        # Edit menu
        self.edit_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.edit_menu.add_command(label="Nächstes Team", command=self.next_folder, state="disabled")
        self.edit_menu.add_command(label="Vorheriges Team", command=self.prev_folder, state="disabled")
        self.edit_menu.add_separator()
        self.edit_menu.add_command(label="Suche Team", command=self.search_folder, state="disabled")
        self.edit_menu.add_separator()
        self.edit_menu.add_command(label="PDF öffnen", command=self.open_pdf, state="disabled")
        self.edit_menu.add_separator()
        self.edit_menu.add_command(label="Code öffnen", command=self.open_code, state="disabled")
        # Add to main menu
        self.menu_bar.add_cascade(label="Navigation", menu=self.edit_menu)

        # View menu
        self.view_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.view_menu.add_checkbutton(label="Übersicht",
                                       command=self.toggle_left_frame)
        self.view_menu.add_checkbutton(label="Test Feedback",
                                       command=self.toggle_right_frame)
        self.menu_bar.add_cascade(label="Ansicht",
                                  menu=self.view_menu)

        # Paned Window
        self.paned_window = tk.PanedWindow(self,
                                           orient="horizontal",
                                           opaqueresize=True,
                                           sashwidth=8,
                                           sashrelief="ridge")
        self.paned_window.pack(fill="both",
                               expand=True)

        # Main frame
        self.main_frame = tk.Frame(self.paned_window)

        self.main_frame_label = tk.Label(self.main_frame,
                                         text="Korrektur",
                                         bd=2,
                                         relief="solid")
        self.main_frame_label.pack(fill="x")

        # Notebook
        self.main_notebook = ttk.Notebook(self.main_frame)
        self.main_notebook.pack(fill="both",
                                expand=True)
        # Scrollbars
        self.main_scroll1 = DoubleScrolledFrame(self.main_notebook)
        self.main_scroll2 = DoubleScrolledFrame(self.main_notebook)
        self.main_notebook.add(self.main_scroll1, text="Punkte")
        self.main_notebook.add(self.main_scroll2, text="Kommentare")

        self.left_frame = tk.Frame(self.paned_window)

        self.left_frame_label = tk.Label(self.left_frame,
                                         text="Übersicht",
                                         bd=2,
                                         relief="solid")
        self.left_frame_label.pack(fill="x")
        self.left_scroll = DoubleScrolledFrame(self.left_frame, width=116)
        self.left_scroll.pack(fill="both",
                              expand=True)

        self.right_frame = tk.Frame(self.paned_window)
        self.right_frame_label = tk.Label(self.right_frame,
                                          text="Test Feedback",
                                          bd=2,
                                          relief="solid")
        self.right_frame_label.pack(fill="x")
        self.right_scroll = DoubleScrolledFrame(self.right_frame, width=116)
        self.right_scroll.pack(fill="both",
                               expand=True)

        self.paned_window.add(self.main_frame)

        # Left frame: parent = self.left_scroll
        self.left_sidebar_frames: list[tk.Frame] = []
        self.left_sidebar_buttons: list[tk.Button] = []
        self._create_team_sidebar_buttons()  # TODO: Remove???

        # Right frame: parent = self.right_scroll
        self.feedback_label = tk.Label(self.right_scroll,
                                       text="",
                                       font=(self.g.test_result_font, self.g.test_result_size),
                                       bg=self.g.right_bar_color,
                                       anchor="w",
                                       justify="left")
        self.feedback_label.pack(fill="both",
                                 padx=10,
                                 pady=10,
                                 expand=True)

        # Main scroll 1: Points --> parent = self.main_scroll1

        # Main scroll 2: Points --> parent = self.main_scroll2

        self.update_graphics()

    def update_graphics(self):
        # Labels
        self.main_frame_label.config(bg=self.g.header_color,
                                     font=(self.g.header_font, self.g.header_size))
        self.left_frame_label.config(bg=self.g.header_color,
                                     font=(self.g.header_font, self.g.header_size))
        self.right_frame_label.config(bg=self.g.header_color,
                                      font=(self.g.header_font, self.g.header_size))

        # Frames
        self.main_frame.config(bg=self.g.main_frame_color)
        self.left_frame.config(bg=self.g.left_bar_color)
        self.right_frame.config(bg=self.g.right_bar_color)
        # Scrollframes --> Canvas config
        self.left_scroll.canvas.config(bg=self.g.left_bar_color)
        self.right_scroll.canvas.config(bg=self.g.right_bar_color)
        self.main_scroll1.canvas.config(bg=self.g.main_frame_color)
        self.main_scroll2.canvas.config(bg=self.g.main_frame_color)

    def toggle_left_frame(self):
        if self.active_left_frame:
            self.paned_window.forget(self.left_frame)
        else:
            self.paned_window.add(self.left_frame, before=self.main_frame)
        # Toggle boolean indicator
        self.active_left_frame = not self.active_left_frame
        self.update_panes()

    def toggle_right_frame(self):
        if self.active_right_frame:
            self.paned_window.forget(self.right_frame)
        else:
            self.paned_window.add(self.right_frame, after=self.main_frame)
        # Toggle boolean indicator
        self.active_right_frame = not self.active_right_frame
        self.update_panes()

    def update_panes(self):
        self.paned_window.paneconfigure(self.main_frame, stretch="always")
        if self.active_left_frame:
            self.paned_window.paneconfigure(self.left_frame, minsize=130, stretch="never")
        if self.active_right_frame:
            self.paned_window.paneconfigure(self.right_frame, minsize=150, stretch="never")

    # TODO: Andere Methoden an die neue Version anpassen
    def save(self):
        """
        Save all states.
        """
        # Save all other data
        if self._ready():
            self.manager.save()

    def open_data(self):
        pass

    def settings_dialog(self):
        """
        Create SettingsDialog.
        """
        SettingsDialog(master=self,
                       name=self.manager.settings.personal_annotation,
                       save_func=self.manager.save_personal_comment)

    def import_dialog(self, allow_folders: bool):
        """
        Create an ImportDialog.
        """
        ImportDialog(master=self,
                     allow_folders=allow_folders,
                     path_to_templates=self.manager.path_to_templates,
                     import_func=self._continue_import)

    def export_data(self):
        """
        Save, Check and Export current states.
        """
        if self._ready():
            self.save()  # Save before exporting
            # Check if all teams were confirmed
            for s in self.manager.states:
                if not s.confirmed:
                    continue_export = messagebox.askokcancel(title="AuD-GUI :D - Warnung!",
                                                             message=f"Team {s.id} wurde noch nicht bestätigt!\n"
                                                                     f"Trotzdem fortfahren?")
                    if not continue_export:
                        return
            # Continue if all teams were confirmed or manually passed to export via messagebox
            ExportDialog(self, export_func=self.manager.export)

    def next_folder(self):
        """
        Switch to the next folder.
        """
        if self._ready():
            self._open_team(min(len(self.manager.states) - 1, self.manager.team_idx + 1))

    def prev_folder(self):
        """
        Switch to the previous folder.
        """
        if self._ready():
            self._open_team(max(0, self.manager.team_idx - 1))

    def search_folder(self):
        """
        Search folder by team ID. Open a dialog to ask for ID.
        """
        if self._ready():
            team_search = simpledialog.askstring(title="Suche Team", prompt="Team-ID eingeben:\t\t\t")
            if team_search is not None:
                found_idx = -1
                for idx, team in enumerate(self.manager.team_list):
                    if team == team_search:
                        found_idx = idx
                        break
                if found_idx == -1:
                    messagebox.showerror(title="AuD-GUI :D - Fehler!", message=f"Team {team_search} nicht gefunden!")
                    return
                else:
                    self._open_team(found_idx)

    def open_pdf(self):
        """
        Open the corresponding PDF file for correction.
        """
        if self._ready():
            self.manager.open_pdf()

    def open_code(self):
        """
        Open the corresponding code folder for correction.
        """
        if self._ready():
            self.manager.open_code()

    def _ready(self):
        """
        Check if the manager has loaded states.

        :return: True if states are loaded, False if not.
        """
        return len(self.manager.states) > 0

    def _continue_import(self, res: list):
        pass

    def _open_team(self):
        pass

    def _switch_confirm(self):
        pass

    def _render_confirm(self):
        pass

    def _increase_task_points(self, class_str: str, task_str: str):
        """
        Increase task points by 0.5 points.

        :param class_str: Class name of the task
        :param task_str: Task name
        """
        self.manager.increase_task_points(class_str, task_str)
        self._render_points_labels()  # Adjust the widgets to match the points of the current state

    def _decrease_task_points(self, class_str: str, task_str: str):
        """
        Decrease task points by 0.5 points.

        :param class_str: Class name of the task
        :param task_str: Task name
        """
        self.manager.decrease_task_points(class_str, task_str)
        self._render_points_labels()  # Adjust the widgets to match the points of the current state

    def _render_points_labels(self):
        """
        Adjust the point label widgets to match the points of the current state.
        """
        pass

    def _render_compile_error(self, frame, button):
        """
        Updates the compile error widgets to match the current state.

        :param frame: Frame containing the compile error button (For coloring)
        :param button: Compile error button (For changing of text)
        """
        pass

    def _switch_compile_error(self, frame, button):
        """
        Switch the compile error state.

        :param frame: Frame containing the compile error button (For coloring)
        :param button: Compile error button (For changing of text)
        """
        pass

    def _create_team_sidebar_buttons(self):
        """
        Create the team buttons on the team sidebar.
        """
        self._delete_team_sidebar_buttons()
        if self._ready():
            for i, t in enumerate(self.manager.team_list):
                f = tk.Frame(self.left_scroll, highlightbackground="lightgray", highlightthickness=2)
                b = tk.Button(f, text=t, command=lambda x=i: self._open_team(index=x))
                b.pack(fill="x")
                f.pack(padx=10, pady=5, fill="x")
                self.left_sidebar_buttons.append(b)
                self.left_sidebar_frames.append(f)
        self.update_graphics()

    def _delete_team_sidebar_buttons(self):
        """
        Delete the existing team side bar buttons.
        """
        if len(self.left_sidebar_frames) > 0:
            for i in self.left_sidebar_frames:
                i.pack_forget()
            self.left_sidebar_frames.clear()
            self.left_sidebar_buttons.clear()

    def _create_feedback_label(self):
        """
        Create the fb label containing the feedback of the automatic test.
        """
        if self.manager.team_state is not None:
            self.feedback_label.config(text=self.manager.team_state.auto_correction_result)
