import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from typing import Union
import os
import json
from abc import abstractmethod

from src.graphics import Graphics


class Window(tk.Tk):
    def __init__(self, title: str = "", size: tuple = (600, 600)):
        """
        Base class for full-size window.

        :param title: Title of the window
        :param size: Size of the window in pixels
        """
        super().__init__()
        # Set window attributes
        self.title(title)
        self.set_size(size)

        # Override the close button action
        self.protocol("WM_DELETE_WINDOW", self.close)

        self.menu_bar = tk.Menu(self)
        self.config(menu=self.menu_bar)

    def set_size(self, size: tuple):
        """
        Set the size of the window.

        :param size: Size of the window in pixels
        """
        assert len(size) == 2
        # Set geometry
        self.geometry(f"{size[0]}x{size[1]}+50+50")

    def close(self):
        """
        Function to save before closing the application
        """
        self.save()
        self.destroy()

    @abstractmethod
    def save(self):
        pass


class DoubleScrolledFrame:
    """
    This frame is used from: https://gist.github.com/novel-yet-trivial/2841b7b640bba48928200ff979204115
    The frame was created by novel-yet-trivial. There is no LICENSE for now.

    A vertically scrolled Frame that can be treated like any other Frame
    ie it needs a master and layout and it can be a master.
    keyword arguments are passed to the underlying Frame
    except the keyword arguments 'width' and 'height', which
    are passed to the underlying Canvas
    note that a widget layed out in this frame will have Canvas as self.master,
    if you subclass this there is no built in way for the children to access it.
    You need to provide the controller separately.
    """

    def __init__(self, master, **kwargs):
        width = kwargs.pop('width', None)
        height = kwargs.pop('height', None)
        self.outer = tk.Frame(master, **kwargs)

        self.vsb = ttk.Scrollbar(self.outer, orient=tk.VERTICAL)
        self.vsb.grid(row=0, column=1, sticky='ns')
        self.hsb = ttk.Scrollbar(self.outer, orient=tk.HORIZONTAL)
        self.hsb.grid(row=1, column=0, sticky='ew')
        self.canvas = tk.Canvas(self.outer, highlightthickness=0, width=width, height=height)
        self.canvas.grid(row=0, column=0, sticky='nsew')
        self.outer.rowconfigure(0, weight=1)
        self.outer.columnconfigure(0, weight=1)
        self.canvas['yscrollcommand'] = self.vsb.set
        self.canvas['xscrollcommand'] = self.hsb.set
        # mouse scroll does not seem to work with just "bind"; You have
        # to use "bind_all". Therefore to use multiple windows you have
        # to bind_all in the current widget
        self.canvas.bind("<Enter>", self._bind_mouse)
        self.canvas.bind("<Leave>", self._unbind_mouse)
        self.vsb['command'] = self.canvas.yview
        self.hsb['command'] = self.canvas.xview

        self.inner = tk.Frame(self.canvas)
        # pack the inner Frame into the Canvas with the topleft corner 4 pixels offset
        self.canvas.create_window(4, 4, window=self.inner, anchor='nw')
        self.inner.bind("<Configure>", self._on_frame_configure)

        self.outer_attr = set(dir(tk.Widget))

    def __getattr__(self, item):
        if item in self.outer_attr:
            # geometry attributes etc (eg pack, destroy, tkraise) are passed on to self.outer
            return getattr(self.outer, item)
        else:
            # all other attributes (_w, children, etc) are passed to self.inner
            return getattr(self.inner, item)

    def _on_frame_configure(self, event=None):
        x1, y1, x2, y2 = self.canvas.bbox("all")
        height = self.canvas.winfo_height()
        width = self.canvas.winfo_width()
        self.canvas.config(scrollregion=(0, 0, max(x2, width), max(y2, height)))

    def _bind_mouse(self, event=None):
        self.canvas.bind_all("<4>", self._on_mousewheel)
        self.canvas.bind_all("<5>", self._on_mousewheel)
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

    def _unbind_mouse(self, event=None):
        self.canvas.unbind_all("<4>")
        self.canvas.unbind_all("<5>")
        self.canvas.unbind_all("<MouseWheel>")

    def _on_mousewheel(self, event):
        """Linux uses event.num; Windows / Mac uses event.delta"""
        func = self.canvas.xview_scroll if event.state & 1 else self.canvas.yview_scroll
        if event.num == 4 or event.delta > 0:
            func(-1, "units")
        elif event.num == 5 or event.delta < 0:
            func(1, "units")

    def __str__(self):
        return str(self.outer)

    # Extra method
    def set_color(self, color: str):
        self.canvas.config(bg=color)
        self.inner.config(bg=color)


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


class ClipboardApp(tk.Frame):
    def __init__(self, master, g: Graphics, path_to_data: str):
        super().__init__(master=master)

        # Variables
        self.data: list[Category] = []
        self.selected_category = -1
        self.g = g
        self.path_to_data_file = path_to_data

        # Widgets
        self.sidebar_buttons: list[tk.Button] = []
        self.sidebar_frames: list[tk.Frame] = []
        self.buttons = []
        self.main_frames = []
        self.labels = []

        # Sidebar
        self.sidebar_frame = tk.Frame(self, highlightbackground=self.g.bg_color, highlightthickness=2)

        self.sidebar_title_frame = tk.Frame(self.sidebar_frame, bg=self.g.bg_color)
        self.sidebar_title = tk.Label(self.sidebar_title_frame,
                                      text="Kategorie",
                                      width=10,
                                      bg=self.g.header_color,
                                      font=(self.g.header_font, self.g.header_size),
                                      relief="solid")
        self.sidebar_title.pack(fill="x",
                                expand=True,
                                side="top",
                                anchor="n")
        # Buttons
        self.sidebar_button_frame = tk.Frame(self.sidebar_title_frame, bg=self.g.bg_color)
        self.plus_button = tk.Button(self.sidebar_button_frame,
                                     text="+",
                                     font=(self.g.points_font, self.g.button_font_size),
                                     command=self.add_category,
                                     bg=self.g.button_color)
        self.buttons.append(self.plus_button)
        self.plus_button.pack(fill="x", side="left", anchor="n", expand=True)
        self.minus_button = tk.Button(self.sidebar_button_frame, text="-",
                                      font=(self.g.points_font, self.g.button_font_size),
                                      command=self.delete_category,
                                      bg=self.g.button_color)
        self.buttons.append(self.minus_button)
        self.minus_button.pack(fill="x", side="right", anchor="n", expand=True)
        self.sidebar_button_frame.pack(fill="x", side="top", anchor="n", expand=True)

        self.sidebar_title_frame.pack(fill="x", side="top", anchor="n")

        self.scroll = DoubleScrolledFrame(self.sidebar_frame, bg=self.g.bg_color,
                                          width=self.sidebar_title.winfo_width())
        self.scroll.pack(fill="both", expand=True)

        self.update_sidebar()

        self.sidebar_frame.pack(fill="both",
                                side="left",
                                anchor="nw")

        # Main frame
        self.main_frame = tk.Frame(self, highlightbackground=self.g.bg_color, highlightthickness=2)

        self.main_title_frame = tk.Frame(self.main_frame, bg=self.g.bg_color)
        self.main_title = tk.Label(self.main_title_frame,
                                   text="Anmerkungen",
                                   bg=self.g.header_color,
                                   font=(self.g.header_font, self.g.header_size),
                                   relief="solid")
        self.main_title.pack(fill="x",
                             expand=True,
                             side="top",
                             anchor="n")

        self.main_title_frame.pack(fill="x", side="top", anchor="n")

        self.add_button = tk.Button(self.main_frame, text="+", font=(self.g.points_font, self.g.button_font_size),
                                    command=self.add_annotation,
                                    bg=self.g.button_color)
        self.buttons.append(self.add_button)
        self.add_button.pack(fill="x")

        self.main_scroll = DoubleScrolledFrame(self.main_frame, bg=self.g.bg_color)
        self.main_scroll.pack(fill="both", expand=True)

        self.update_main_frame()

        self.main_frame.pack(fill="both",
                             side="right",
                             anchor="ne",
                             expand=True)

        # Load stored data
        self.load()
        self.bind("<Configure>", self.wrap_labels)

    def update_sidebar(self):
        # Forget old content
        for f in self.sidebar_frames:
            f.pack_forget()
        self.sidebar_frames.clear()

        # Create new content
        for i, c in enumerate(self.data):
            f = tk.Frame(self.scroll, highlightbackground=self.g.bg_color, highlightthickness=5)
            b = tk.Button(f, text=c.title, command=lambda x=i: self.open_category(x),
                          width=max([len(i.title) for i in self.data]),
                          bg=self.g.button_color, font=(self.g.points_font, self.g.button_font_size))
            self.buttons.append(b)
            b.pack(fill="x", expand=True)
            f.pack(fill="x", padx=2, pady=2, side="top", anchor="n", expand=True)
            self.sidebar_frames.append(f)
            self.sidebar_buttons.append(b)
        self.color_sidebar()

    def color_sidebar(self):
        for i in range(len(self.sidebar_frames)):
            if i == self.selected_category:
                self.sidebar_frames[i].configure(highlightbackground="blue")
            else:
                self.sidebar_frames[i].configure(highlightbackground=self.g.bg_color)
        self.scroll.set_color(self.g.bg_color)

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
        self.main_scroll.set_color(self.g.bg_color)
        if len(self.main_frames) > 0:
            for f in self.main_frames:
                f.pack_forget()
            self.main_frames.clear()
            self.labels.clear()

        if self.selected_category >= 0:
            for an in self.data[self.selected_category].annotations:
                f = tk.Frame(self.main_scroll,
                             bg=self.g.bg_color,
                             highlightbackground=self.g.button_color,
                             highlightthickness=2)
                b0 = tk.Button(f, text="-", width=5,
                               command=lambda x=an: self.delete_annotation(x),
                               bg=self.g.button_color,
                               font=(self.g.points_font, self.g.button_font_size))
                self.buttons.append(b0)
                text = tk.Label(f, text=an, justify="left", bg=self.g.bg_color,
                                font=(self.g.points_font, self.g.task_font_size))
                self.labels.append(text)
                b1 = tk.Button(f, text="Copy", width=7,
                               command=lambda x=an: self.copy_to_clipboard(x),
                               bg=self.g.button_color, font=(self.g.points_font, self.g.button_font_size))
                self.buttons.append(b1)
                b0.pack(side="left", fill="y")
                text.pack(side="left", fill="y")
                b1.pack(side="right", fill="y")
                f.pack(fill="x", anchor="w", side="top")
                self.main_frames.append(f)
            self.wrap_labels(None)

    def update_labels_graphics(self):
        self.config(bg=self.g.bg_color)
        self.scroll.set_color(self.g.bg_color)
        self.main_scroll.set_color(self.g.bg_color)
        for i in self.buttons:
            i.config(bg=self.g.button_color,
                     font=(self.g.points_font, self.g.button_font_size))
        for i in self.labels:
            i.config(bg=self.g.bg_color,
                     font=(self.g.points_font, self.g.task_font_size))
        for i in self.main_frames:
            i.config(bg=self.g.bg_color,
                     highlightbackground=self.g.button_color)

        self.sidebar_title.config(bg=self.g.header_color,
                                  font=(self.g.header_font, self.g.header_size))
        self.main_title.config(bg=self.g.header_color,
                               font=(self.g.header_font, self.g.header_size))

    def wrap_labels(self, event):
        if event is None or event.widget == self:
            for i, f in enumerate(self.main_frames):
                width = self.winfo_width() - self.sidebar_frame.winfo_width() - 180
                self.labels[i].configure(wraplength=width)

    def add_annotation(self):
        if self.selected_category >= 0:
            annotation = simpledialog.askstring(title="Anmerkung hinzufügen", prompt="Text:" + "\t" * 10, parent=self)
            if annotation is not None:
                self.data[self.selected_category].add_annotation(annotation)
                self.update_main_frame()

    def delete_annotation(self, x: str):
        if self.selected_category >= 0:
            permission = messagebox.askyesno(title="Anmerkung entfernen",
                                             message=f"Anmerkung \"{x}\" unwiderruflich löschen?",
                                             parent=self)
            if permission:
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
