import os
import tkinter as tk
import platform
from tkinter import simpledialog
from tkinter import messagebox

from gui_utils import ScrollFrame
from dialogs import ImportDialog, SettingsDialog, ExportDialog
from manager import Manager


class Window(tk.Tk):
    def __init__(self, title: str = "", size: tuple = (600, 600)):
        """
        Base class for full-size window.

        :param title: Title of the window
        :param size: Size of the window in pixels
        """
        super().__init__()
        # Set window to fullscreen
        if platform.system() == "Darwin":  # macOS
            self.attributes("-zoomed", True)
        else:  # Windows and some Linux distributions
            self.state("zoomed")
        # Set window attributes
        self.title(title)
        self.set_size(size)

    def set_size(self, size: tuple):
        """
        Set the size of the window.

        :param size: Size of the window in pixels
        """
        assert len(size) == 2
        # Set geometry
        self.geometry(f"{size[0]}x{size[1]}+50+50")


class AuDGUI(Window):
    def __init__(self):
        """
        Class containing all GUI widgets, which send commands to the manager class
        """
        super().__init__(title="AuD-GUI :D")

        # Manager class to execute the widget commands
        self.manager = Manager(path_of_mainfile=os.path.dirname(__file__))

        # Override the close button action
        self.protocol("WM_DELETE_WINDOW", self.close)

        # Construct menu -----------------------------------------------------------------------------------------------
        self.menu_bar = tk.Menu(self)

        # File menu
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.file_menu.add_command(label="Korrektur öffnen", command=self.open_data)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Abgaben importieren", command=self.import_dialog)
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
        # Add to main menu
        self.menu_bar.add_cascade(label="Navigation", menu=self.edit_menu)

        # Set menu
        self.config(menu=self.menu_bar)
        # --------------------------------------------------------------------------------------------------------------

        # Team Sidebar -------------------------------------------------------------------------------------------------
        # Widget lists for team sidebar
        self.team_sidebar_buttons = []
        self.team_sidebar_frames = []

        self.EXPANDED_TEAM_SIDEBAR = 158  # Width of the team side bar in pixels
        self.team_sidebar_container = tk.Frame(self, bg="lightgray")
        # Title frame
        self.team_sidebar_title_container = tk.Frame(self.team_sidebar_container, bg="gray")
        # Title
        self.team_sidebar_title = tk.Label(self.team_sidebar_title_container,
                                           text="Übersicht",
                                           font=("Arial", 18),
                                           bg="gray",
                                           bd=2,
                                           relief="solid",
                                           width=10)
        self.team_sidebar_button = tk.Button(self.team_sidebar_title_container,
                                             text="▶",
                                             font=("Arial", 13),
                                             bg="gray",
                                             bd=2,
                                             relief="solid",
                                             command=self._switch_team_sidebar)

        self.team_sidebar_scroll = ScrollFrame(self.team_sidebar_container,
                                               width=self.EXPANDED_TEAM_SIDEBAR,
                                               bg="lightgray")

        self._team_sidebar_expanded = True
        self._toggle_team_sidebar(state=True)  # Button widgets are created here

        # Main Frame ---------------------------------------------------------------------------------------------------
        # Widgets for Main Frame
        self.main_frames = []
        self.total_points_label = None
        self.class_points_labels = []
        self.task_points_labels = []
        self.confirm_button = None

        self.main_container = tk.Frame(self, bg="lightgray")
        # Title frame
        self.main_title_container = tk.Frame(self.main_container, bg="gray")
        # Title
        self.main_title = tk.Label(self.main_title_container,
                                   text="Korrektur",
                                   font=("Arial", 18),
                                   bg="gray",
                                   bd=2,
                                   relief="solid")
        # Main Scrollframe containing the buttons
        self.main_scroll = ScrollFrame(self.main_container,
                                       bg="lightgray",
                                       factor=1.5)
        # Pack widgets
        self.main_title.pack(fill="x", side="left", anchor="w", expand=True)
        self.main_title_container.pack(fill="x", side="top", anchor="n")

        # Setup the main frame
        self._create_main_frame()
        # Pack the scrollframe and then the whole frame
        self.main_scroll.pack(fill="both", expand=True)
        self.main_container.pack(fill="both", expand=True, side="left", anchor="w")

        # Feedback (fb) Sidebar ----------------------------------------------------------------------------------------
        # Widgets for fb sidebar
        self.feedback_label = None

        self.EXPANDED_FB_SIDEBAR = 500  # Width of the fb sidebar in pixels

        self.fb_sidebar_container = tk.Frame(self, bg="lightgray")
        # Title frame
        self.fb_sidebar_title_container = tk.Frame(self.fb_sidebar_container, bg="gray")
        # Title
        self.fb_sidebar_title = tk.Label(self.fb_sidebar_title_container,
                                         text="Rückmeldung",
                                         font=("Arial", 18),
                                         bg="gray",
                                         bd=2,
                                         relief="solid",
                                         width=20)
        self.fb_sidebar_button = tk.Button(self.fb_sidebar_title_container,
                                           text="◀",
                                           font=("Arial", 13),
                                           bg="gray",
                                           bd=2,
                                           relief="solid",
                                           command=self._switch_fb_sidebar)

        # Scrollframe of the fb sidebar containing the label
        self.fb_sidebar_scroll = ScrollFrame(self.fb_sidebar_container,
                                             width=self.EXPANDED_FB_SIDEBAR,
                                             bg="lightgray",
                                             factor=1.5)

        self._fb_sidebar_expanded = True
        self._toggle_fb_sidebar(state=True)  # fb label is created here

    def _create_main_frame(self):
        """
        Delete existing main frame and constructing new frame based on the loaded team state.
        """
        parent = self.main_scroll.frame()  # Just to make things easier
        # Delete existing widgets
        if len(self.main_frames) > 0:
            for i in self.main_frames:
                i.pack_forget()
            self.main_frames.clear()
            self.class_points_labels.clear()
            self.task_points_labels.clear()
        # Create new widgets
        if self._ready():
            # ID title and buttons
            main_title_frame = tk.Frame(parent, bg="lightgray")
            # ID Label
            main_id = tk.Label(main_title_frame,
                               text=f"Team {self.manager.get_id()}",
                               bg="lightgray",
                               font=("Arial", 26),
                               anchor="w")
            main_id.pack(fill="x", side="left", anchor="w", padx=10, pady=10, expand=True)
            # Next button
            next_button = tk.Button(main_title_frame,
                                    text="Weiter",
                                    font=("Arial", 16),
                                    command=self.next_folder)
            next_button.pack(fill="x", padx=10, side="right", anchor="e")
            # Previous button
            prev_button = tk.Button(main_title_frame,
                                    text="Zurück",
                                    font=("Arial", 16),
                                    command=self.prev_folder)
            prev_button.pack(fill="x", padx=10, side="right", anchor="e")
            # Pack
            main_title_frame.pack(fill="x", pady=10, expand=True, anchor="w")
            self.main_frames.append(main_title_frame)  # Store for faster deletion

            # Compile Error frame
            compile_error_frame = tk.Frame(parent, bg="lightgray")
            compile_error_label = tk.Label(compile_error_frame,
                                           text="Compile Error: ",
                                           font=("Arial", 12),
                                           bg="lightgray",
                                           anchor="w")
            compile_error_label.pack(side="left", anchor="w", padx=10, pady=10)
            compile_error_button_frame = tk.Frame(compile_error_frame,
                                                  bg="lightgray",
                                                  highlightbackground="green",
                                                  highlightthickness=2)
            compile_error_button = tk.Button(compile_error_button_frame,
                                             text="Nein",
                                             font=("Arial", 12),
                                             width=20,
                                             command=lambda: self._switch_compile_error(compile_error_button_frame,
                                                                                        compile_error_button))
            self._render_compile_error(compile_error_button_frame, compile_error_button)  # Ensure correct state
            compile_error_button.pack(fill="x", expand=True)
            compile_error_button_frame.pack(side="left", pady=10)

            compile_error_frame.pack(fill="x", pady=10)
            self.main_frames.append(compile_error_frame)  # Store for faster deletion

            # Total points
            p = self.manager.get_total_points()
            self.total_points_label = tk.Label(parent,
                                               text=f"Total: {p['actual']} / {p['max']}",
                                               bg="lightgray",
                                               anchor="w",
                                               font=("Arial", 16))
            self.total_points_label.pack(fill="x", padx=10, pady=10)
            self.main_frames.append(self.total_points_label)  # Store for faster deletion

            # Classes and corresponding tasks
            for c in self.manager.team_state.comment["classes"]:
                c_title, c_points = c["title"], c["points"]
                c_label = tk.Label(parent,
                                   text=f"{c_title}: {c_points['actual']} / {c_points['max']}",
                                   bg="lightgray",
                                   anchor="w",
                                   font=("Arial", 14))
                self.class_points_labels.append((c_title, c_label))  # Store for correct config when changing points
                c_label.pack(fill="x", anchor="w", padx=10, pady=10)
                self.main_frames.append(c_label)  # Store for faster deletion

                # Tasks
                for t in self.manager.team_state.comment["classes"][self.manager.get_class_idx(c_title)]["tasks"]:
                    t_title, t_points = t["title"], t["points"]
                    # Task frame
                    t_frame = tk.Frame(parent, bg="lightgray")
                    # Minus button
                    t_minus_button = tk.Button(t_frame,
                                               text="-",
                                               command=lambda x=(c_title, t_title): self._decrease_task_points(x[0],
                                                                                                               x[1]))
                    t_minus_button.pack(side="left", anchor="w", fill="x", pady=5, padx=5)
                    # Points label
                    t_points_label = tk.Label(t_frame,
                                              text=f"{t_points['actual']} / {t_points['max']}",
                                              bg="lightgray",
                                              font=("Arial", 12))
                    t_points_label.pack(fill="x", side="left", padx=5, pady=5)
                    self.task_points_labels.append((c_title, t_title, t_points_label))  # Store for changing points text
                    # Plus button
                    t_plus_button = tk.Button(t_frame,
                                              text="+",
                                              command=lambda x=(c_title, t_title): self._increase_task_points(x[0],
                                                                                                              x[1]))
                    t_plus_button.pack(side="left", fill="x", pady=5, padx=5)
                    # Description label
                    t_desc_label = tk.Label(t_frame,
                                            text=t_title,
                                            bg="lightgray",
                                            font=("Arial", 12))
                    t_desc_label.pack(fill="x", side="left", padx=5, pady=5)
                    t_frame.pack(fill="x", padx=10, anchor="w")
                    self.main_frames.append(t_frame)  # Store for faster deletion

            # Confirm button
            self.confirm_button = tk.Button(parent,
                                            text="Nicht bestätigt",
                                            bg="#ffcccb",
                                            width=20,
                                            font=("Arial", 16),
                                            command=self._switch_confirm)
            self.confirm_button.pack(fill="x", padx=10, pady=10, anchor="w", side="left")
            self._render_confirm()  # Ensure correct state
            self.main_frames.append(self.confirm_button)  # Store for faster deletion

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

    def _render_compile_error(self, frame, button):
        """
        Updates the compile error widgets to match the current state.

        :param frame: Frame containing the compile error button (For coloring)
        :param button: Compile error button (For changing of text)
        """
        if self.manager.get_compile_error():
            frame.configure(highlightbackground="red")
            button.configure(text="Ja")
        else:
            frame.configure(highlightbackground="green")
            button.configure(text="Nein")

    def _switch_compile_error(self, frame, button):
        """
        Switch the compile error state.

        :param frame: Frame containing the compile error button (For coloring)
        :param button: Compile error button (For changing of text)
        """
        self.manager.switch_compile_error()
        self._render_compile_error(frame, button)  # Update Compile Error button
        self._render_points_labels()  # Update labels

    def _switch_team_sidebar(self):
        """
        Switch state of team sidebar to (not) collapsed.
        """
        self._toggle_team_sidebar(state=not self._team_sidebar_expanded)

    def _toggle_team_sidebar(self, state: bool):
        """
        Set the team sidebar to a specified state.

        :param state: Expanded (True) or collapsed (False)
        """
        if not state:
            self._team_sidebar_expanded = False
            # Collapse sidebar
            self.team_sidebar_button.configure(text="▶")
            self.team_sidebar_title.pack_forget()
            self.team_sidebar_scroll.pack_forget()
            self.team_sidebar_button.pack(side="right", anchor="e")
            self.team_sidebar_title_container.pack(fill="x", side="top", anchor="n")
            self.team_sidebar_container.pack(fill="y", expand=False, side="left", anchor="w")
        else:
            self._team_sidebar_expanded = True
            # Forget previous layout
            self.team_sidebar_button.pack_forget()
            # Construct expanded sidebar
            self.team_sidebar_button.configure(text="◀")
            self.team_sidebar_button.pack(side="right", anchor="e")
            self.team_sidebar_title.pack(fill="both", side="left", anchor="w", expand=True)
            self.team_sidebar_title_container.pack(fill="x", side="top", anchor="n")
            # Setup the sidebar buttons
            self._create_team_sidebar_buttons()
            self.team_sidebar_scroll.pack(fill="both", expand=True)
            self.team_sidebar_container.pack(fill="y", expand=False, side="left", anchor="w")

    def _switch_fb_sidebar(self):
        """
        Switch state of fb sidebar to (not) collapsed.
        """
        self._toggle_fb_sidebar(state=not self._fb_sidebar_expanded)

    def _toggle_fb_sidebar(self, state: bool):
        """
        Set the fb sidebar to a specified state.

        :param state: Expanded (True) or collapsed (False)
        """
        if not state:
            self._fb_sidebar_expanded = False
            # Collapse sidebar
            self.fb_sidebar_button.configure(text="◀")
            self.fb_sidebar_title.pack_forget()
            self.fb_sidebar_scroll.pack_forget()
            self.fb_sidebar_button.pack(side="left", anchor="w")
            self.fb_sidebar_title_container.pack(fill="x", side="top", anchor="n")
            self.fb_sidebar_container.pack(fill="y", expand=False, side="right", anchor="e")
        else:
            self._fb_sidebar_expanded = True
            # Forget previous layout
            self.fb_sidebar_button.pack_forget()
            # Construct expanded sidebar
            self.fb_sidebar_button.configure(text="▶")
            self.fb_sidebar_button.pack(side="left", anchor="w")
            self.fb_sidebar_title.pack(fill="both", side="right", anchor="e", expand=True)
            self.fb_sidebar_title_container.pack(fill="x", side="top", anchor="n")
            # Setup the sidebar label
            self._create_feedback_label()
            self.fb_sidebar_scroll.pack(fill="both", expand=True)
            self.fb_sidebar_container.pack(fill="y", expand=False, side="right", anchor="e")

    def _create_team_sidebar_buttons(self):
        """
        Create the team buttons on the team sidebar.
        """
        # Delete previous sidebar
        self._delete_team_sidebar_buttons()
        self.team_sidebar_scroll.re_init()
        # Create new sidebar based on team_list
        if self._ready():
            for i, t in enumerate(self.manager.team_list):
                f = tk.Frame(self.team_sidebar_scroll.frame(), highlightbackground="lightgray", highlightthickness=2)
                b = tk.Button(f, text=t, command=lambda x=i: self._open_team(index=x))
                b.pack(fill="x")
                f.pack(padx=10, pady=5, fill="x")
                self.team_sidebar_buttons.append(b)
                self.team_sidebar_frames.append(f)
        self._color_sidebar()

    def _delete_team_sidebar_buttons(self):
        """
        Delete the existing team side bar buttons.
        """
        # Delete previous sidebar
        if len(self.team_sidebar_frames) > 0:
            for i in self.team_sidebar_frames:
                i.pack_forget()
            self.team_sidebar_frames.clear()
            self.team_sidebar_buttons.clear()
            self.team_sidebar_scroll.frame().pack_forget()
            self.team_sidebar_scroll.pack_forget()

    def _create_feedback_label(self):
        """
        Create the fb label containing the feedback of the automatic test.
        """
        self._delete_feedback_label()
        self.fb_sidebar_scroll.re_init()
        # Create new feedback label
        if self.manager.team_state is not None:
            self.feedback_label = tk.Label(self.fb_sidebar_scroll.frame(),
                                           text=self.manager.team_state.auto_correction_result,
                                           bg="lightgray",
                                           anchor="w",
                                           justify="left",
                                           font=("Arial", 12),
                                           wraplength=self.EXPANDED_FB_SIDEBAR)
            self.feedback_label.pack(fill="both", padx=10, pady=10, expand=True)

    def _delete_feedback_label(self):
        """
        Delete the existing fb label.
        """
        if self.feedback_label is not None:
            self.feedback_label.pack_forget()
            self.fb_sidebar_scroll.frame().pack_forget()
            self.fb_sidebar_scroll.pack_forget()

    def _open_team(self, index: int):
        """
        Open team specified by a list index.

        :param index: List index of the team in state list of the manager.
        """
        self.manager.open_team(index)
        # Update labels
        self._create_main_frame()
        self._switch_fb_sidebar()
        self._switch_fb_sidebar()
        self._color_sidebar()
        # Save if old team was opened
        self.save()

    def _color_sidebar(self):
        """
        Adjust the color of sidebar buttons and frames to match the current state.
        """
        if len(self.team_sidebar_frames) > 0 and len(self.team_sidebar_buttons) > 0:
            # Color frames for "log in"-theme
            for i in self.team_sidebar_frames:
                i.configure(highlightbackground="lightgray")
            self.team_sidebar_frames[self.manager.team_idx].configure(highlightbackground="blue")
            # Color buttons for "confirmed"-theme
            for idx, i in enumerate(self.team_sidebar_buttons):
                if self.manager.states[idx].confirmed:
                    i.configure(bg="lightgreen")
                else:
                    i.configure(bg="lightgray")

    def _continue_import(self, res: list):
        """
        Callback function for import dialog. Continues in manager and then updates the widgets.

        :param res: List containing data for the import manager
        """
        # Load directory
        self.manager.import_data(res)
        # Change status back and forth to refresh scroll region (call 2 times)
        self._switch_team_sidebar()
        self._switch_team_sidebar()
        # Start with first team
        self._open_team(index=0)

        # Update menu
        if len(os.listdir(self.manager.path_to_data)) > 0:
            self.file_menu.entryconfigure("Korrektur öffnen", state="normal")
        # Configure export menu
        self.file_menu.entryconfigure("Korrekturen exportieren", state="normal")
        # Update edit menu
        for i in ["Nächstes Team", "Vorheriges Team", "Suche Team", "PDF öffnen"]:
            self.edit_menu.entryconfigure(i, state="normal")

    def _ready(self):
        """
        Check if the manager has loaded states.

        :return: True if states are loaded, False if not.
        """
        return len(self.manager.states) > 0

    def import_dialog(self):
        """
        Create an ImportDialog.
        """
        ImportDialog(master=self,
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

    def settings_dialog(self):
        """
        Create SettingsDialog.
        """
        SettingsDialog(master=self,
                       name=self.manager.settings.personal_annotation,
                       save_func=self.manager.save_personal_comment)

    def open_data(self):
        """
        Open data and update widgets if loading was successful.
        """
        # Set team_ids
        success = self.manager.open_data()
        if success:
            # Change status back and forth to refresh scroll region (call 2 times)
            self._switch_team_sidebar()
            self._switch_team_sidebar()
            # Start with first team
            self._open_team(index=0)

            # Configure menu
            self.file_menu.entryconfigure("Korrekturen exportieren", state="normal")
            # Update edit menu
            for i in ["Nächstes Team", "Vorheriges Team", "Suche Team", "PDF öffnen"]:
                self.edit_menu.entryconfigure(i, state="normal")

    def close(self):
        """
        Function to save before closing the application
        """
        self.save()
        self.destroy()

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

    def open_pdf(self):
        """
        Open the corresponding PDF file for correction.
        """
        if self._ready():
            self.manager.open_pdf()

    def save(self):
        """
        Save all states.
        """
        if self._ready():
            self.manager.save()


if __name__ == '__main__':
    # Let the magic happen...
    AuDGUI().mainloop()
