import tkinter as tk


class ScrollFrame(tk.Frame):
    def __init__(self, parent, width: int = -1, height: int = 400, factor: float = 1, **kwargs):
        """
        Construct a scrollable frame on a canvas basis.

        :param parent: Parent frame of the scroll frame
        :param width: Width of the scrollable container in pixels
        :param height: Height of the scrollable container in pixels
        :param kwargs: Other specifications for tkinter frames
        """
        super().__init__(parent, **kwargs)
        self.width = width
        self.height = height
        self.factor = factor
        self.kwargs = kwargs
        self._renew_scrollframe()

    def _renew_scrollframe(self):
        if self.width == -1:
            self._canvas = tk.Canvas(self, height=self.height, **self.kwargs)
        else:
            self._canvas = tk.Canvas(self, width=self.width, height=self.height, **self.kwargs)
        self._sidebar_frame = tk.Frame(self._canvas, **self.kwargs)
        self._sidebar_frame.bind("<Configure>", lambda e: self.update_scrollregion())
        self._canvas.bind("<Configure>", self._on_canvas_configure)
        self._canvas.bind("<Enter>", lambda e: self._bind_mousewheel(True))
        self._canvas.bind("<Leave>", lambda e: self._bind_mousewheel(False))
        self._canvas.create_window((0, 0), window=self._sidebar_frame, anchor="nw")

        # Vertical scrollbar
        self._v_scrollbar = tk.Scrollbar(self, orient="vertical", command=self._canvas.yview)
        self._v_scrollbar.pack(side="right", fill="y")
        self._canvas.configure(yscrollcommand=self._v_scrollbar.set)

        # Horizontal scrollbar
        self._h_scrollbar = tk.Scrollbar(self, orient="horizontal", command=self._canvas.xview)
        self._h_scrollbar.pack(side="bottom", fill="x")
        self._canvas.configure(xscrollcommand=self._h_scrollbar.set)

        self._canvas.pack(side="left", fill="both", expand=True)

    def re_init(self):
        self._canvas.pack_forget()
        self._h_scrollbar.pack_forget()
        self._v_scrollbar.pack_forget()
        self._sidebar_frame.pack_forget()
        self._renew_scrollframe()

    def _on_canvas_configure(self, event):
        # Adjust the width of sidebar_frame to match the width of the canvas
        canvas_width = event.width
        if self.width == -1:
            self._canvas.itemconfig(self._canvas.create_window((0, 0), window=self._sidebar_frame, anchor="nw"))
        else:
            self._canvas.itemconfig(self._canvas.create_window((0, 0), window=self._sidebar_frame, anchor="nw"),
                                    width=self.factor * canvas_width)

    def _on_mousewheel(self, event):
        # Check if Shift is held for horizontal scroll, otherwise use vertical scroll
        if event.state & 0x0001:  # Shift is held down
            self._canvas.xview_scroll(-1 * int(event.delta / 120), "units")
        else:
            self._canvas.yview_scroll(-1 * int(event.delta / 120), "units")

    def _bind_mousewheel(self, state: bool):
        if state:
            self._canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        else:
            self._canvas.unbind_all("<MouseWheel>")

    def update_scrollregion(self):
        self._canvas.configure(scrollregion=self._canvas.bbox("all"))

    def pack(self, **kw):
        self._sidebar_frame.pack(**kw)
        super().pack(**kw)

    def frame(self) -> tk.Frame:
        """
        :return: The frame in which all scrollable widgets should be packed. This frame also has to be packed.
        The parent is the scroll frame itself.
        """
        return self._sidebar_frame
