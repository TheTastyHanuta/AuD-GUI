import json
import os
from tkinter import font


class Graphics:
    def __init__(self, filepath: str = "", json_file: str = ""):
        if json_file != "":
            # Initialization via json dict
            with open(json_file, "r", encoding="utf-8") as f:
                json_data = json.load(f)
                self.__dict__.update(json_data)
        else:
            self.graphics_path = os.path.join(filepath, "graphics.json")

            # Font types
            self.header_font = "Arial"
            self.test_result_font = "Arial"
            self.points_font = "Arial"

            # Font sizes
            self.header_size = 16
            self.test_result_size = 12
            self.team_title_size = 26
            self.button_font_size = 16

            self.total_points_size = 18
            self.class_font_size = 14
            self.task_font_size = 14

            # Headers
            self.header_color = "#004a9f"
            # Main frame
            self.bg_color = "#8c9fb1"
            # Buttons
            self.button_color = "#2f586e"

    def get_available_fonts(self):
        return list(font.families())

    def set_fonts(self, fonts: list[str]):
        # Check if realizable => Check with common fonts
        fs = self.get_available_fonts()
        for i in range(len(fonts)):
            if fonts[i] not in fs:
                fonts[i] = "Arial"  # default Arial

        self.header_font = fonts[0]
        self.test_result_font = fonts[1]
        self.points_font = fonts[2]

    def set_sizes(self, sizes: list[int]):
        # Font sizes => Are restricted to [8, 26] by the scrollboxes
        self.header_size = sizes[0]
        self.test_result_size = sizes[1]
        self.team_title_size = sizes[2]
        self.button_font_size = sizes[3]

        self.total_points_size = sizes[4]
        self.class_font_size = sizes[5]
        self.task_font_size = sizes[6]

    def set_color(self, colors: list[str]):
        # Check validity
        for i, c in enumerate(colors):
            if not c.startswith("#"):
                c = "#" + c
            if len(c) != 7:
                c = "#ffffff"  # default white
            colors[i] = c

        # Headers
        self.header_color = colors[0]
        # Main frame
        self.bg_color = colors[1]
        # Buttons
        self.button_color = colors[2]

    def save(self):
        """
        Saves the settings as JSON file at the location stored in settings_path
        """
        with open(self.graphics_path, "w", encoding="utf-8") as f:
            json.dump(self.__dict__, f, indent=4, ensure_ascii=False)
