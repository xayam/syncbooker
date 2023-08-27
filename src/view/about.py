import os
import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
from tkinter import font
from PIL import ImageTk, Image

from model.l18n import *


class About:

    def __init__(self, app):
        self.app = app
        self.about = tk.Toplevel(self.app.root)
        self.about.title(MENU_HELP_ABOUT[self.app.locale])
        if os.path.exists(self.app.ICON_ICO):
            self.about.iconbitmap(self.app.ICON_ICO)
        self.about.minsize(width=500, height=200)
        self._create_about()
        self.show_about()

    def show_about(self):
        self.about.grab_set()
        self.about.mainloop()

    def _create_about(self):
        self.about_frame_title = tk.Frame(self.about, height=32)
        self.about_frame_title.pack(fill=tk.X, expand=False)
        self.bold32 = font.Font(self.about_frame_title, font="Arial", size=32, weight=font.BOLD)
        self.about_title = tk.Label(self.about_frame_title,
                                    text=f"{self.app.NAME} v{self.app.VERSION} (64-bit)",
                                    font=self.bold32)
        self.about_title.pack(fill=tk.X, side=tk.LEFT, expand=False, padx=10, pady=5)
        self.about_tabs = ttk.Notebook(self.about)
        self.about_tabs.pack(fill=tk.BOTH, expand=True, pady=5)
        self.about_tab_about = tk.Frame(self.about_tabs)
        self.about_tab_about.pack(fill=tk.BOTH, expand=True)
        self.about_tab_license = tk.Frame(self.about_tabs)
        self.about_tab_license.pack(fill=tk.BOTH, expand=True)
        self.about_tabs.add(self.about_tab_about, text=MENU_HELP_ABOUT[self.app.locale])
        self.about_tabs.add(self.about_tab_license, text=ABOUT_LICENSE[self.app.locale])

        self.about_frame_icon = tk.Frame(self.about_tab_about, width=64)
        self.about_frame_icon.pack(fill=tk.Y, side=tk.LEFT, expand=False, padx=5, pady=5)
        self.about_icon = ImageTk.PhotoImage(Image.open(self.app.ICON_PNG).resize((64, 64)))
        self.about_label_icon = tk.Label(master=self.about_frame_icon, image=self.about_icon, width=64)
        self.about_label_icon.pack()
        self.about_frame_annot = tk.Frame(self.about_tab_about)
        self.about_frame_annot.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        self.about_annotation1 = tk.Label(self.about_frame_annot,
                                          wraplength=350, justify="left",
                                          text=ABOUT_SYNCBOOKER[self.app.locale],
                                          font=("Arial", 14))
        self.about_annotation1.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.about_annotation2 = tk.Label(self.about_frame_annot,
                                          fg="blue", cursor="hand2", anchor=tk.W,
                                          text=self.app.GITHUB_SYNCBOOKER)
        self.about_annotation2.pack(fill=tk.X, expand=False, padx=5, pady=5)
        self.about_annotation2.bind("<1>", func=lambda _: os.startfile(self.app.GITHUB_SYNCBOOKER))
        self.about_annotation3 = tk.Label(self.about_frame_annot,
                                          fg="blue", cursor="hand2", anchor=tk.W,
                                          text=self.app.SYNCBOOKER_CHAT)
        self.about_annotation3.pack(fill=tk.X, expand=False, padx=5, pady=5)
        self.about_annotation3.bind("<1>", func=lambda _: os.startfile(self.app.SYNCBOOKER_CHAT))
        self.about_annotation4 = tk.Label(self.about_frame_annot,
                                          fg="blue", cursor="hand2", anchor=tk.W,
                                          text=self.app.EMAIL)
        self.about_annotation4.pack(fill=tk.X, expand=False, padx=5, pady=5)
        self.about_annotation4.bind("<1>", func=lambda _: os.startfile("mailto:" + self.app.EMAIL))

        self.about_license = scrolledtext.ScrolledText(self.about_tab_license,
                                                       wrap=tk.WORD, width=42, height=11,
                                                       font=("Arial", 14))
        self.about_license.pack(expand=False, pady=5)
        if os.path.exists(self.app.LICENSE):
            with open(self.app.LICENSE, mode="r", encoding="UTF-8") as txt:
                self.license = txt.read()
            self.about_license.insert(tk.END, self.license)
        else:
            self.about_license.insert(tk.END, ABOUT_LICENSE_NOTFOUND)
