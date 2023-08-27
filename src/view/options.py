import os
import tkinter as tk
from model.l18n import *
# from tkinter import ttk
# from tkinter import scrolledtext
# from tkinter import font
# from PIL import ImageTk, Image


class Options:

    def __init__(self, app):
        self.app = app
        self.options = tk.Toplevel(self.app.root)
        self.options.title(MENU_SERVICE_OPTIONS[self.app.locale])
        if os.path.exists(self.app.ICON_ICO):
            self.options.iconbitmap(self.app.ICON_ICO)
        self.options.minsize(width=500, height=300)
        self._create_options()
        self.show_options()

    def _create_options(self):
        self.label_options = tk.Label(self.options, text="В разработке")
        self.label_options.pack(fill=tk.BOTH, expand=True)

    def show_options(self):
        self.options.grab_set()
        self.options.mainloop()
