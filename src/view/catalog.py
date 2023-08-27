import os
import tkinter as tk
from model.l18n import *
# from tkinter import ttk
# from tkinter import scrolledtext
# from tkinter import font
# from PIL import ImageTk, Image


class Catalog:

    def __init__(self, app):
        self.app = app
        self.catalog = tk.Toplevel(self.app.root)
        self.catalog.title(MENU_SERVICE_CATALOG[self.app.locale])
        if os.path.exists(self.app.ICON_ICO):
            self.catalog.iconbitmap(self.app.ICON_ICO)
        self.catalog.minsize(width=500, height=300)
        self._create_catalog()
        self.show_catalog()

    def _create_catalog(self):
        self.label_catalog = tk.Label(self.catalog, text="В разработке")
        self.label_catalog.pack(fill=tk.BOTH, expand=True)

    def show_catalog(self):
        self.catalog.grab_set()
        self.catalog.mainloop()
