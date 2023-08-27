import os
import tkinter as tk
from controller.realization import Realization
from model.l18n import *


class Menu(Realization):

    def __init__(self, app):

        self.app = app
        self._create_menu()
        self._bind_menu()

        Realization.__init__(self, app=self)

    def _bind_menu(self):
        self.app.root.bind("<Control-q>", self.menu_file_quit_click)
        self.app.root.bind("<F1>", self.menu_help_faq_click)

    def _create_menu(self):
        self.menu = tk.Menu(master=self.app.root, bg="red")
        self.app.root.config(menu=self.menu)

        self.menu_file = tk.Menu(self.menu, tearoff=0)
        # self.menu_file.add_command(label="Open folder book...")
        # self.menu_file.add_command(label="Export...")
        self.menu_file.add_command(label=MENU_FILE_QUIT[self.app.locale],
                                   command=self.menu_file_quit_click,
                                   accelerator="Ctrl+Q")
        self.menu.add_cascade(label=MENU_FILE[self.app.locale],
                              menu=self.menu_file,
                              accelerator="Alt+F")

        # self.menu_edit = tk.Menu(self.menu, tearoff=0)
        # self.menu_edit.add_command(label="Restart")
        # self.menu_edit.add_command(label="Stop")
        # self.menu_edit.add_command(label="Restart all")
        # self.menu_edit.add_command(label="Stop all")
        # self.menu.add_cascade(label="Edit", menu=self.menu_edit)

        self.menu_service = tk.Menu(self.menu, tearoff=0)
        self.menu_service_lang = tk.IntVar(self.menu)
        state_lang = 0 if self.app.locale == RU else 1
        self.menu_service_lang.set(state_lang)
        self.menu_service.add_radiobutton(label=RU, value=0, variable=self.menu_service_lang,
                                          command=lambda: self.menu_service_language(RU))
        self.menu_service.add_radiobutton(label=EN, value=1, variable=self.menu_service_lang,
                                          command=lambda: self.menu_service_language(EN))
        self.menu_service.add_separator()
        self.menu_service.add_command(label=MENU_SERVICE_CATALOG[self.app.locale] + "...",
                                      command=self.menu_service_catalog_click)
        self.menu_service.add_command(label=MENU_SERVICE_OPTIONS[self.app.locale] + "...",
                                      command=self.menu_service_options_click)
        # self.menu_service.add_command(label="Create own sync book...")
        self.menu.add_cascade(label=MENU_SERVICE[self.app.locale], menu=self.menu_service)

        self.menu_help = tk.Menu(self.menu, tearoff=0)
        self.menu_help.add_command(label=MENU_HELP_FAQ[self.app.locale], accelerator="F1",
                                   command=self.menu_help_faq_click)
        self.menu_help.add_command(label=MENU_HELP_CASES[self.app.locale],
                                   command=lambda: os.startfile(self.app.CASES_HTML))
        self.menu_help.add_command(label="README.md",
                                   command=lambda: os.startfile(self.app.README_MD))
        self.menu_help.add_command(label=MENU_HELP_UPDATES[self.app.locale],
                                   command=self.menu_help_updates_click)
        self.menu_help.add_command(label=MENU_HELP_DONATE[self.app.locale],
                                   command=lambda: os.startfile(self.app.DONATE))
        self.menu_help.add_command(label=MENU_HELP_ABOUT[self.app.locale] + "...",
                                   command=self.menu_help_about_click)
        self.menu.add_cascade(label=MENU_HELP[self.app.locale],
                              menu=self.menu_help,
                              accelerator="Alt+H")
