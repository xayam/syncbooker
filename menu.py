import os
import tkinter as tk
from commands import Commands
from l18n import *


class Menu(Commands):

    def __init__(self, root: tk.Tk):

        self.root = root
        # self._create_menu()
        # self._bind_menu()

    def _bind_menu(self):
        self.root.bind("<Control-q>", self.menu_file_exit_click)
        self.root.bind("<F1>", self.menu_help_faq_click)

    def _create_menu(self):
        self.menu = tk.Menu(master=self.root, bg="red")
        self.root.config(menu=self.menu)

        self.menu_file = tk.Menu(self.menu, tearoff=0)
        self.menu_file.add_command(label="Open folder book...")
        self.menu_file.add_command(label="Export...")
        self.menu_file.add_command(label=MENU_FILE_EXIT[LOCALE], command=self.menu_file_exit_click, accelerator="Ctrl+Q")
        self.menu.add_cascade(label="File", menu=self.menu_file, accelerator="Alt+F")

        self.menu_edit = tk.Menu(self.menu, tearoff=0)
        self.menu_edit.add_command(label="Restart")
        self.menu_edit.add_command(label="Stop")
        self.menu_edit.add_command(label="Restart all")
        self.menu_edit.add_command(label="Stop all")
        self.menu.add_cascade(label="Edit", menu=self.menu_edit)

        self.menu_service = tk.Menu(self.menu, tearoff=0)
        self.menu_service.add_command(label="Options...")
        self.menu_service.add_command(label="Create own sync book...")
        self.menu.add_cascade(label="Service", menu=self.menu_service)

        self.menu_help = tk.Menu(self.menu, tearoff=0)
        self.menu_help.add_command(label="FAQ...", accelerator="F1",
                                   command=self.menu_help_faq_click)
        self.menu_help.add_command(label="Cases...",
                                   command=lambda: os.startfile(os.getcwd() + f"/../cases.html"))
        self.menu_help.add_command(label="README.md...",
                                   command=lambda: os.startfile(os.getcwd() + f"/../README.md"))
        self.menu_help.add_command(label="Check updates...")
        self.menu_help.add_command(label="Donate...")
        self.menu_help.add_command(label=MENU_HELP_ABOUT[LOCALE],
                                   command=self.menu_help_about_click)
        self.menu.add_cascade(label="Help", menu=self.menu_help)

    def menu_file_exit_click(self, event=None):
        self.root.quit()

    def menu_help_faq_click(self, event=None):
        os.startfile(os.getcwd() + f"/../faq.html")

    def menu_help_about_click(self, event=None):
        print("menu_help_about_click")

    def toolbar_options_click(self, event=None):
        print("toolbar_options_click")
