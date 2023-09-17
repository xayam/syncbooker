import os
import tkinter as tk
from PIL import ImageTk, Image
from model.utils import *
from model.l18n import *
from .menu import Menu
from .toolbar import ToolBar
from .statusbar import StatusBar
from .scroll import VerticalScrolledFrame


class Sceleton(Menu, StatusBar, ToolBar):

    def __init__(self, app):
        self.app = app
        self.loading = True
        self.frame_content1 = None
        self.frame_content2 = None
        self.right_cover_label = None
        self.annotation_text_area1 = None
        self.annotation_text_area2 = None
        self.annotation_frame = None
        self.current_index = None
        self.frames_left = []
        self.covers_label = []
        self.covers = []
        self.desc_label = []
        self.author_label = []
        self.bookname_label = []
        self.current_select = ''
        self.current_dir = None
        self.start_index = 0
        self.current_time = 0
        self.frame_left_list = None
        self.frame_empty_list = None
        self.annotation = ''
        self.eng_sync = None
        self.rus_sync = None
        self.micro = None
        self.frame_right_annotation1 = None
        self.annotation_text = None
        self.frame_right_annotation2 = None
        self.annotation_text_area = None
        self.annotation_text_area_other = None
        self.eng_book = ''
        self.rus_book = ''
        self.sync = None
        self.book = None
        self.book_other = None
        self.sync_other = None

        self._create_sceleton()
        self._create_left_list()

        Menu.__init__(self, app=self)
        StatusBar.__init__(self, app=self)
        ToolBar.__init__(self, app=self)

    def _create_sceleton(self):
        self.sceleton_toolbar = tk.Frame(master=self.app.root, height=48)
        self.sceleton_toolbar.pack(fill=tk.X)
        self.sceleton_main = tk.Frame(master=self.app.root, bg="gray")

        self.sceleton_main.pack(fill=tk.BOTH, expand=True)
        self.sceleton_statusbar = tk.Frame(master=self.app.root, height=32)
        self.sceleton_statusbar.pack(fill=tk.X, side=tk.BOTTOM)

        self.sceleton_table = tk.Frame(master=self.sceleton_main)
        self.sceleton_table.pack(fill=tk.BOTH, expand=True)

        self.sceleton_splitter_vertical1 = tk.Frame(master=self.sceleton_table)

        self.sceleton_services = tk.Frame(master=self.sceleton_splitter_vertical1)
        self.sceleton_ads = tk.Frame(master=self.sceleton_splitter_vertical1)
        self.sceleton_services.pack(fill=tk.BOTH, expand=True)
        self.sceleton_ads.pack(fill=tk.X, side=tk.BOTTOM)

        self.sceleton_table1 = tk.Frame(master=self.sceleton_table)
        self.sceleton_table2 = tk.Frame(master=self.sceleton_table)
        self.sceleton_splitter_vertical1.grid(row=0, column=0, sticky="nsew")
        self.sceleton_table1.grid(row=0, column=1, sticky="nsew")
        self.sceleton_table2.grid(row=0, column=2, sticky="nsew")
        self.sceleton_table.grid_columnconfigure(1, weight=1, uniform="group1")
        self.sceleton_table.grid_columnconfigure(2, weight=1, uniform="group1")
        self.sceleton_table.grid_rowconfigure(0, weight=1)

    def _create_left_list(self):
        msg = SCELETON_DATA_NOT_FOUND[self.app.locale]
        if os.path.exists("../data/"):
            msg = SCELETON_BOOKS_NOT_FOUND[self.app.locale]
            dir1 = os.scandir("../data/")
            for surname in dir1:
                if surname.is_dir():
                    names = surname.name.split("_-_")
                    self.app.books.append({"surname": names[0],
                                           "book": names[1],
                                           "full": surname.name})

        if self.app.books:
            self.frame_left_list = VerticalScrolledFrame(self.sceleton_services)
            self.frame_left_list.pack(fill=tk.BOTH, expand=True)
            for book in self.app.books:
                try:
                    if len(self.app.option[POSITIONS][book["full"]]) > 0:
                        pass
                except KeyError:
                    self.app.option[POSITIONS][book["full"]] = {POSI: "0\n0.0\n0.0", AUDIO: EN}

                self.frames_left.append(tk.Frame(master=self.frame_left_list.interior))
                self.frames_left[-1].pack(fill=tk.X, anchor="w", expand=True, padx=5, pady=5)
                self.covers.append(ImageTk.PhotoImage(
                    Image.open("../data/" + book["surname"] + "_-_" + book["book"] + "/cover.jpg").resize((150, 150))))
                self.covers_label.append(tk.Label(master=self.frames_left[-1], cursor="hand2",
                                                  text=book["surname"] + "_-_" + book["book"],
                                                  background="gray",
                                                  image=self.covers[-1], height=150))
                self.covers_label[-1].pack(fill=tk.Y, side=tk.LEFT, expand=True)
                self.covers_label[-1].bindtags(["left_listbox_onselect"])
                self.covers_label[-1].bind_class("left_listbox_onselect", '<Button-1>',
                                                 self.app.left_listbox_onselect)
                self.desc_label.append(tk.Frame(master=self.frames_left[-1], width="150", height=150))
                self.desc_label[-1].pack(fill=tk.Y, side=tk.LEFT, expand=True)
                self.author_label.append(tk.Label(master=self.desc_label[-1],
                                                  wraplength=150,
                                                  height=3,
                                                  text=book["surname"].replace("_", " ")))
                self.author_label[-1].pack(fill=tk.X, side=tk.TOP, expand=False)
                self.bookname_label.append(tk.Label(master=self.desc_label[-1],
                                                    wraplength=150,
                                                    height=3,
                                                    text=book["book"].replace("_", " ")))
                self.bookname_label[-1].pack(fill=tk.X, side=tk.TOP, expand=False)
        else:
            self.frame_empty_list = tk.Label(master=self.sceleton_services, text=msg)
            self.frame_empty_list.pack(fill=tk.BOTH, side=tk.TOP, expand=True)
