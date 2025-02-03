import tkinter as tk
from tkinter import messagebox, simpledialog
from tkinter import ttk
import os

from src.gui_utils import Window, DoubleScrolledFrame, ClipboardApp
from src.manager import Manager
from src.dialogs import ImportDialog, ExportDialog, SettingsDialog, GraphicsDialog


class AuDGUI(Window):
    def __init__(self, start_path: str):
        """
        Class containing all GUI widgets, which send commands to the manager class
        """
        super().__init__(title="AuD-GUI :D")
        self.main_path = start_path

        self.manager = Manager(path_of_mainfile=self.main_path)

        self.g = self.manager.graphics  # Set graphics

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
        if len(os.listdir(self.manager.path_to_data)) <= 1:
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
                                       command=self._toggle_left_frame)
        self.view_menu.add_checkbutton(label="Test Feedback",
                                       command=self._toggle_right_frame)
        self.view_menu.add_separator()
        self.view_menu.add_command(label="Grafik-Einstellungen",
                                   command=self.graphics_dialog)
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
        self.main_notebook.add(self.main_scroll1, text="Punkte")

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

        # Right frame: parent = self.right_scroll
        self.feedback_label = tk.Label(self.right_scroll,
                                       text="",
                                       anchor="w",
                                       justify="left")
        self.feedback_label.pack(fill="both",
                                 padx=10,
                                 pady=10,
                                 expand=True)

        # Main scroll 1: Points --> parent = self.main_scroll1
        self.total_points_label = None
        self.class_points_labels = []
        self.task_points_labels = []
        self.compile_error_button = None
        self.plag_button = None
        self.confirm_button = None

        self.main_frames: list[tk.Frame] = []
        self.main_total_points_labels: list[tk.Label] = []
        self.main_class_title_labels: list[tk.Label] = []
        self.main_task_points_labels: list[tk.Label] = []
        self.main_buttons: list[tk.Button] = []
        # ID title and buttons
        self.main_title_frame = tk.Frame(self.main_scroll1)
        # ID Label
        self.main_id = tk.Label(self.main_title_frame,
                                text=f"Team ID",
                                anchor="w")
        self.main_id.pack(fill="x",
                          side="left",
                          anchor="w",
                          padx=10,
                          pady=10,
                          expand=True)
        # Next button
        self.next_button = tk.Button(self.main_title_frame,
                                     text="Weiter",
                                     command=self.next_folder)
        self.next_button.pack(fill="x",
                              padx=10,
                              side="right",
                              anchor="e")
        # Previous button
        self.prev_button = tk.Button(self.main_title_frame,
                                     text="Zurück",
                                     command=self.prev_folder)
        self.prev_button.pack(fill="x",
                              padx=10,
                              side="right",
                              anchor="e")
        # Pack
        self.main_title_frame.pack(fill="x",
                                   pady=10,
                                   expand=True,
                                   anchor="w")

        # Login Label
        self.login_label = tk.Label(self.main_scroll1,
                                    text=f"StudOn-Kennungen: ",
                                    anchor="w")
        self.login_label.pack(fill="x",
                              side="top",
                              anchor="w",
                              padx=10,
                              expand=True)

        # Main scroll 2: Points --> parent = self.main_scroll2
        self.clipboard_helper = ClipboardApp(self.main_notebook,
                                             self.g,
                                             self.manager.path_to_clipboarddata)
        # self.clipboard_helper.pack(fill="both", expand=True)
        self.main_notebook.add(self.clipboard_helper, text="Kommentare")

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
        self.main_frame.config(bg=self.g.bg_color)
        self.left_frame.config(bg=self.g.bg_color)
        self.right_frame.config(bg=self.g.bg_color)
        # Left sidebar frames
        self._color_sidebar()

        # Scrollframes --> Canvas/inner config
        self.left_scroll.set_color(self.g.bg_color)
        self.right_scroll.set_color(self.g.bg_color)
        self.main_scroll1.set_color(self.g.bg_color)

        # Main frame
        self.main_title_frame.config(bg=self.g.bg_color)
        self.main_id.config(bg=self.g.bg_color,
                            font=(self.g.points_font, self.g.team_title_size))
        self.login_label.config(bg=self.g.bg_color,
                                font=(self.g.points_font, self.g.total_points_size))
        self.next_button.config(bg=self.g.button_color,
                                font=(self.g.points_font, self.g.button_font_size))
        self.prev_button.config(bg=self.g.button_color,
                                font=(self.g.points_font, self.g.button_font_size))
        for i in self.main_frames:
            i.config(bg=self.g.bg_color)
        for i in self.main_total_points_labels:
            i.config(bg=self.g.bg_color,
                     font=(self.g.points_font, self.g.total_points_size))
        for i in self.main_class_title_labels:
            i.config(bg=self.g.bg_color,
                     font=(self.g.points_font, self.g.class_font_size))
        for i in self.main_task_points_labels:
            i.config(bg=self.g.bg_color,
                     font=(self.g.points_font, self.g.task_font_size))
        for i in self.main_buttons:
            i.config(bg=self.g.button_color,
                     font=(self.g.points_font, self.g.button_font_size))

        if self.confirm_button is not None:
            self.confirm_button.config(font=(self.g.points_font, self.g.button_font_size))
        if self.compile_error_button is not None:
            self.compile_error_button.config(font=(self.g.points_font, self.g.button_font_size))
        if self.plag_button is not None:
            self.plag_button.config(font=(self.g.points_font, self.g.button_font_size))
        self.feedback_label.config(font=(self.g.test_result_font, self.g.test_result_size),
                                   bg=self.g.bg_color)

        self.clipboard_helper.update_labels_graphics()

    def _delete_main_frame(self):
        for li in [self.main_frames,
                   self.main_total_points_labels,
                   self.main_class_title_labels,
                   self.main_task_points_labels,
                   self.main_buttons]:
            if len(li) > 0:
                for i in li:
                    i.pack_forget()
                li.clear()

        # Delete lists for point <-> label relations
        self.class_points_labels.clear()
        self.task_points_labels.clear()

        if self.confirm_button is not None:
            self.confirm_button.pack_forget()
            self.confirm_button = None
        if self.compile_error_button is not None:
            self.compile_error_button.pack_forget()
            self.compile_error_button = None
        if self.plag_button is not None:
            self.plag_button.pack_forget()
            self.plag_button = None

    def _create_main_frame(self):
        self._delete_main_frame()

        # Create new widgets
        if self._ready():
            self.main_id.config(text=f"Team {self.manager.get_id()}")
            self.login_label.config(text=f"StudOn-Kennungen: {', '.join(self.manager.get_logins())}")

            # Plagiat Error frame --------------------------------------------------------------------------------------
            plag_frame = tk.Frame(self.main_scroll1,
                                  bd=2,
                                  relief="solid")
            plag_label = tk.Label(plag_frame,
                                  text="Plagiat: ",
                                  anchor="w",
                                  width=12)
            plag_label.pack(side="left",
                            anchor="w",
                            padx=10,
                            pady=10)
            self.plag_button = tk.Button(plag_frame,
                                         text="Nein",
                                         width=10,
                                         command=self._switch_plag)
            self._render_plag()  # Ensure correct state
            self.plag_button.pack(side="right",
                                  padx=10,
                                  pady=10)
            plag_frame.pack(fill="x",
                            side="top",
                            pady=10)
            self.main_frames.append(plag_frame)
            self.main_total_points_labels.append(plag_label)

            # Compile Error frame --------------------------------------------------------------------------------------
            compile_error_frame = tk.Frame(self.main_scroll1,
                                           bd=2,
                                           relief="solid")
            compile_error_label = tk.Label(compile_error_frame,
                                           text="Compile Error: ",
                                           anchor="w",
                                           width=12)
            compile_error_label.pack(side="left",
                                     anchor="w",
                                     padx=10,
                                     pady=10)
            self.compile_error_button = tk.Button(compile_error_frame,
                                                  text="Nein",
                                                  width=10,
                                                  command=self._switch_compile_error)
            self._render_compile_error()  # Ensure correct state
            self.compile_error_button.pack(side="right",
                                           padx=10,
                                           pady=10)
            compile_error_frame.pack(fill="x",
                                     side="top",
                                     pady=10)
            self.main_frames.append(compile_error_frame)
            self.main_total_points_labels.append(compile_error_label)

            # Total points ---------------------------------------------------------------------------------------------
            p = self.manager.get_total_points()
            total_points_frame = tk.Frame(self.main_scroll1,
                                          relief="solid",
                                          bd=2)
            self.total_points_label = tk.Label(total_points_frame,
                                               text=f"Total: {p['actual']} / {p['max']}",
                                               anchor="w")
            self.total_points_label.pack(fill="x",
                                         padx=10,
                                         pady=10)
            total_points_frame.pack(fill="x",
                                    side="top",
                                    pady=10)
            self.main_total_points_labels.append(self.total_points_label)
            self.main_frames.append(total_points_frame)

            # Classes --------------------------------------------------------------------------------------------------
            for c in self.manager.team_state.comment["classes"]:
                c_title, c_points = c["title"], c["points"]
                c_label = tk.Label(self.main_scroll1,
                                   text=f"{c_title}: {c_points['actual']} / {c_points['max']}",
                                   anchor="w",
                                   relief="solid",
                                   bd=1)
                self.class_points_labels.append((c_title, c_label))  # Store for correct config when changing points
                c_label.pack(fill="x",
                             anchor="w",
                             padx=10,
                             pady=10)
                self.main_class_title_labels.append(c_label)
                # Tasks ------------------------------------------------------------------------------------------------
                for t in self.manager.team_state.comment["classes"][self.manager.get_class_idx(c_title)]["tasks"]:
                    t_title, t_points = t["title"], t["points"]
                    # Task frame
                    t_frame = tk.Frame(self.main_scroll1)
                    # Minus button
                    t_minus_button = tk.Button(t_frame,
                                               text="-",
                                               command=lambda x=(c_title, t_title): self._decrease_task_points(x[0],
                                                                                                               x[1]))
                    t_minus_button.pack(side="left",
                                        anchor="w",
                                        fill="x",
                                        pady=5,
                                        padx=5)
                    # Points label
                    t_points_label = tk.Label(t_frame,
                                              text=f"{t_points['actual']} / {t_points['max']}")
                    t_points_label.pack(fill="x",
                                        side="left",
                                        padx=5,
                                        pady=5)
                    self.task_points_labels.append((c_title, t_title, t_points_label))  # Store for changing points text
                    # Plus button
                    t_plus_button = tk.Button(t_frame,
                                              text="+",
                                              command=lambda x=(c_title, t_title): self._increase_task_points(x[0],
                                                                                                              x[1]))
                    t_plus_button.pack(side="left",
                                       fill="x",
                                       pady=5,
                                       padx=5)
                    # Description label
                    t_desc_label = tk.Label(t_frame,
                                            text=t_title)
                    t_desc_label.pack(fill="x",
                                      side="left",
                                      padx=5,
                                      pady=5)
                    t_frame.pack(fill="x",
                                 padx=10,
                                 anchor="w")
                    self.main_frames.append(t_frame)
                    self.main_task_points_labels += [t_points_label, t_desc_label]
                    self.main_buttons += [t_plus_button, t_minus_button]

            # Confirm button -------------------------------------------------------------------------------------------
            self.confirm_button = tk.Button(self.main_scroll1,
                                            text="Nicht bestätigt",
                                            bg="#ffcccb",
                                            width=20,
                                            command=self._switch_confirm)
            self.confirm_button.pack(fill="x", padx=10, pady=10, anchor="w", side="left")
            self._render_confirm()  # Ensure correct state

            # Color everything
            self.update_graphics()

    def _toggle_left_frame(self):
        if self.active_left_frame:
            self.paned_window.forget(self.left_frame)
        else:
            self.paned_window.add(self.left_frame, before=self.main_frame)
        # Toggle boolean indicator
        self.active_left_frame = not self.active_left_frame
        self._update_panes()

    def _toggle_right_frame(self):
        if self.active_right_frame:
            self.paned_window.forget(self.right_frame)
        else:
            self.paned_window.add(self.right_frame, after=self.main_frame)
        # Toggle boolean indicator
        self.active_right_frame = not self.active_right_frame
        self._update_panes()

    def _update_panes(self):
        self.paned_window.paneconfigure(self.main_frame, stretch="always")
        if self.active_left_frame:
            self.paned_window.paneconfigure(self.left_frame, minsize=130, stretch="never")
        if self.active_right_frame:
            self.paned_window.paneconfigure(self.right_frame, minsize=150, stretch="never")

    def _color_sidebar(self):
        """
        Adjust the color of sidebar buttons and frames to match the current state.
        """
        if len(self.left_sidebar_frames) > 0 and len(self.left_sidebar_buttons) > 0:
            # Color frames for "log in"-theme
            for i in self.left_sidebar_frames:
                i.configure(highlightbackground=self.g.bg_color)
            self.left_sidebar_frames[self.manager.team_idx].configure(highlightbackground="blue")
            # Color buttons for "confirmed"-theme
            for idx, i in enumerate(self.left_sidebar_buttons):
                if self.manager.states[idx].confirmed:
                    i.configure(bg="lightgreen")
                else:
                    i.configure(bg=self.g.button_color)

    def save(self):
        """
        Save all states.
        """
        # Save all other data
        if self._ready():
            self.manager.save()
        self.clipboard_helper.save()

    def open_data(self):
        # Set team_ids
        success = self.manager.open_data()
        if success:
            # Change status back and forth to refresh scroll region (call 2 times)
            self._create_team_sidebar_buttons()
            self._create_feedback_label()
            # Start with first team
            self._open_team(index=0)

            # Configure menu
            self.file_menu.entryconfigure("Korrekturen exportieren", state="normal")
            # Update edit menu
            for i in ["Nächstes Team", "Vorheriges Team", "Suche Team", "PDF öffnen", "Code öffnen"]:
                self.edit_menu.entryconfigure(i, state="normal")

    def settings_dialog(self):
        """
        Create SettingsDialog.
        """
        SettingsDialog(master=self,
                       input_list=[self.manager.settings.compile_error_annotation,
                                   self.manager.settings.plagiat_annotation,
                                   self.manager.settings.personal_annotation,
                                   self.manager.settings.id_key],
                       g=self.g,
                       save_func=self.manager.save_personal_comment)

    def graphics_dialog(self):
        """
        Create GraphicsDialog.
        """
        GraphicsDialog(master=self,
                       g=self.g,
                       save_func=self._save_graphics)

    def _save_graphics(self, fonts: list[str], sizes: list[int], colors: list[str]):
        self.manager.save_graphics(fonts, sizes, colors)
        self.update_graphics()

    def import_dialog(self, allow_folders: bool):
        """
        Create an ImportDialog.
        """
        ImportDialog(master=self,
                     allow_folders=allow_folders,
                     path_to_templates=self.manager.path_to_templates,
                     g=self.g,
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
            ExportDialog(self, g=self.g, export_func=self.manager.export)

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
        self.manager.team_idx = 0
        # Load directory
        self.manager.import_data(res)
        # Change status back and forth to refresh scroll region (call 2 times)
        self._create_team_sidebar_buttons()
        self._create_feedback_label()
        # Start with first team
        self._open_team(index=0)

        # Update menu
        if len(os.listdir(self.manager.path_to_data)) > 0:
            self.file_menu.entryconfigure("Korrektur öffnen", state="normal")
        # Configure export menu
        self.file_menu.entryconfigure("Korrekturen exportieren", state="normal")
        # Update edit menu
        for i in ["Nächstes Team", "Vorheriges Team", "Suche Team", "PDF öffnen", "Code öffnen"]:
            self.edit_menu.entryconfigure(i, state="normal")

    def _open_team(self, index: int):
        # Save if old team was opened
        self.save()

        self.manager.open_team(index)
        # Update labels
        self._create_main_frame()
        # self._color_sidebar()
        self._create_feedback_label()
        self._color_sidebar()

    def _switch_confirm(self):
        """
        Switch the confirm state.
        """
        self.manager.team_state.confirmed = not self.manager.team_state.confirmed
        self._render_confirm()  # Change widgets

    def _render_confirm(self):
        """
        Change the widget states to be consistent with the confirm flag.
        """
        if self.manager.team_state.confirmed:
            self.confirm_button.configure(text="Bestätigt", bg="lightgreen")
        else:
            self.confirm_button.configure(text="Nicht bestätigt", bg="#ffcccb")
        self._color_sidebar()  # Colors the team sidebar buttons

    def _increase_task_points(self, class_str: str, task_str: str):
        """
        Increase task points by 0.5 points.

        :param class_str: Class name of the task
        :param task_str: Task name
        """
        # Switch confirmed to prevent errors
        if self.manager.team_state.confirmed:
            self._switch_confirm()

        self.manager.increase_task_points(class_str, task_str)
        self._render_points_labels()  # Adjust the widgets to match the points of the current state

    def _decrease_task_points(self, class_str: str, task_str: str):
        """
        Decrease task points by 0.5 points.

        :param class_str: Class name of the task
        :param task_str: Task name
        """
        # Switch confirmed to prevent errors
        if self.manager.team_state.confirmed:
            self._switch_confirm()

        self.manager.decrease_task_points(class_str, task_str)
        self._render_points_labels()  # Adjust the widgets to match the points of the current state

    def _render_points_labels(self):
        """
        Adjust the point label widgets to match the points of the current state.
        """
        if self.total_points_label is not None:
            # Update and retrieve total points
            self.manager.update_total_points()
            p = self.manager.get_total_points()
            self.total_points_label.configure(text=f"Total: {p['actual']} / {p['max']}")
            # Update class labels
            for t, i in self.class_points_labels:
                p = self.manager.get_class_points(t)
                i.configure(text=f"{t}: {p['actual']} / {p['max']}")
            # Update task labels
            for c, t, i in self.task_points_labels:
                p = self.manager.get_task_points(c, t)
                i.configure(text=f"{p['actual']} / {p['max']}")

    def _switch_compile_error(self):
        """
        Switch the compile error state.
        """
        # Switch confirmed to prevent errors
        if self.manager.team_state.confirmed:
            self._switch_confirm()

        self.manager.switch_compile_error()
        self._render_compile_error()  # Update Compile Error button
        self._render_points_labels()  # Update labels

    def _render_compile_error(self):
        """
        Updates the compile error widgets to match the current state.
        """
        if self.compile_error_button is not None:
            if self.manager.get_compile_error():
                self.compile_error_button.configure(text="Ja", bg="red")
            else:
                self.compile_error_button.configure(text="Nein", bg="green")

    def _switch_plag(self):
        """
        Switch the plagiat state.
        """
        # Switch confirmed to prevent errors
        if self.manager.team_state.confirmed:
            self._switch_confirm()

        self.manager.switch_plagiat()
        self._render_plag()  # Update plag button
        self._render_points_labels()  # Update labels

    def _render_plag(self):
        """
        Updates the compile error widgets to match the current state.
        """
        if self.plag_button is not None:
            if self.manager.get_plagiat():
                self.plag_button.configure(text="Ja", bg="red")
            else:
                self.plag_button.configure(text="Nein", bg="green")

    def _create_team_sidebar_buttons(self):
        """
        Create the team buttons on the team sidebar.
        """
        self._delete_team_sidebar_buttons()
        if self._ready():
            for i, t in enumerate(self.manager.team_list):
                f = tk.Frame(self.left_scroll, highlightbackground=self.g.bg_color, highlightthickness=2)
                b = tk.Button(f, text=t, width=11, command=lambda x=i: self._open_team(index=x))
                b.pack(fill="x", expand=True)
                f.pack(padx=10, pady=5, fill="x", expand=True)
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
