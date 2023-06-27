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
        self.root.bind("<F1>", self.menu_help_doc_click)

    def _create_menu(self):
        self.menu = tk.Menu(master=self.root, bg="red")
        self.root.config(menu=self.menu)

        self.menu_file = tk.Menu(self.menu, tearoff=0)
        self.menu_file.add_command(label="Открыть...")
        self.menu_file.add_command(label="Новый")
        self.menu_file.add_command(label="Сохранить...")
        self.menu_file.add_command(label=MENU_FILE_EXIT(), command=self.menu_file_exit_click, accelerator="Ctrl+Q")
        self.menu.add_cascade(label="Файл", menu=self.menu_file, accelerator="Alt+F")

        self.menu_edit = tk.Menu(self.menu, tearoff=0)
        self.menu_edit.add_command(label="Возобновить")
        self.menu_edit.add_command(label="Остановить")
        self.menu_edit.add_command(label="Возобновить всё")
        self.menu_edit.add_command(label="Остановить всё")
        self.menu.add_cascade(label="Правка", menu=self.menu_edit)

        self.menu_view = tk.Menu(self.menu, tearoff=0)
        self.menu_view.add_command(label="Статистика")
        self.menu.add_cascade(label="Вид", menu=self.menu_view)

        self.menu_service = tk.Menu(self.menu, tearoff=0)
        self.menu_service.add_command(label="Создать...")
        self.menu_service.add_command(label="Настройки")
        self.menu.add_cascade(label="Сервис", menu=self.menu_service)

        self.menu_help = tk.Menu(self.menu, tearoff=0)
        self.menu_help.add_command(label="Документация", command=self.menu_help_doc_click, accelerator="F1")
        self.menu_help.add_command(label="Помощь")
        self.menu_help.add_command(label=MENU_HELP_ABOUT())
        self.menu.add_cascade(label="Справка", menu=self.menu_help)

    def menu_file_exit_click(self, event=None):
        self.root.quit()

    def menu_help_doc_click(self, event=None):
        print("menu_help_doc_click")

    def toolbar_options_click(self, event=None):
        print("toolbar_options_click")
