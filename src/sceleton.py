import json
import os
import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
from PIL import ImageTk, Image
import pygame
from consts import *
from menu import Menu
from toolbar import ToolBar
from statusbar import StatusBar
from scroll import VerticalScrolledFrame


class Sceleton(Menu, ToolBar, StatusBar):

    def __init__(self, root: tk.Tk):
        self.root = root
        self.books = []
        self.frame_content1 = None
        self.frame_content2 = None
        self.right_cover_label = None
        self.annotation_text_area1 = None
        self.annotation_text_area2 = None
        self.annotation_frame = None
        self.current_index = None

        self._create_sceleton()

    def _create_sceleton(self):
        self.russian = "Русский"
        self.english = "English"
        self.audio_lang = tk.StringVar(value=self.english)

        self.sceleton_toolbar = tk.Frame(master=self.root, height=48)
        self.sceleton_toolbar.pack(fill=tk.X)
        self.sceleton_main = tk.Frame(master=self.root, bg="gray")

        self.sceleton_main.pack(fill=tk.BOTH, expand=True)
        self.sceleton_statusbar = tk.Frame(master=self.root, height=32)
        self.sceleton_statusbar.pack(fill=tk.X)

        self.sceleton_splitter_vertical1 = tk.Frame(master=self.sceleton_main, width=300)
        self.sceleton_splitter_vertical1.pack(fill=tk.Y, side=tk.LEFT, expand=True)
        self.sceleton_services = tk.Frame(master=self.sceleton_splitter_vertical1)
        self.sceleton_ads = tk.Frame(master=self.sceleton_splitter_vertical1)
        self.sceleton_services.pack(fill=tk.BOTH, expand=True)
        self.sceleton_ads.pack(fill=tk.X, side=tk.BOTTOM)

        self.sceleton_table = tk.Frame(master=self.sceleton_main)
        self.sceleton_table.pack(fill=tk.BOTH, expand=True)
        self.sceleton_table1 = tk.Frame(master=self.sceleton_table)
        self.sceleton_table2 = tk.Frame(master=self.sceleton_table)
        self.sceleton_table1.grid(row=0, column=0, sticky="nsew")
        self.sceleton_table2.grid(row=0, column=1, sticky="nsew")
        self.sceleton_table.grid_columnconfigure(0, weight=1, uniform="group1")
        self.sceleton_table.grid_columnconfigure(1, weight=1, uniform="group1")
        self.sceleton_table.grid_rowconfigure(0, weight=1)

        self.recreate_left_list()

    def recreate_left_list(self):
        self.books = []
        msg = "Папка ./data не найдена"
        if os.path.exists("data/"):
            msg = "Книги в папке ./data не найдены"
            dir1 = os.scandir("data/")
            for surname in dir1:
                if surname.is_dir():
                    names = surname.name.split("_-_")
                    self.books.append({"surname": names[0], "book": names[1]})

        if self.books:
            self.options = {"fg": "black", "bg": "white", "fontsize": 20,
                            "positions": ["" for _ in range(len(self.books))]}

            self.frame_left_list = VerticalScrolledFrame(self.sceleton_services)
            self.frame_left_list.pack(fill=tk.BOTH, expand=True)
            self.frames_left = []
            self.covers_label = []
            self.covers = []
            self.desc_label = []
            self.author_label = []
            self.bookname_label = []
            for book in self.books:
                self.frames_left.append(tk.Frame(master=self.frame_left_list.interior))
                self.frames_left[-1].pack(fill=tk.X, anchor="w", expand=True, padx=5, pady=5)
                self.covers.append(ImageTk.PhotoImage(
                    Image.open("data/" + book["surname"] + "_-_" + book["book"] + "/cover.jpg").resize((150, 150))))
                self.covers_label.append(tk.Label(master=self.frames_left[-1], cursor="hand2",
                                                  text=book["surname"] + "_-_" + book["book"],
                                                  background="gray",
                                                  image=self.covers[-1], height=150))
                self.covers_label[-1].pack(fill=tk.Y, side=tk.LEFT, expand=True)
                self.covers_label[-1].bindtags(["left_listbox_onselect"])
                self.covers_label[-1].bind_class("left_listbox_onselect", '<Button-1>',
                                                 self.left_listbox_onselect)
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
            Menu.__init__(self, self.root)
            ToolBar.__init__(self, self.root, self.sceleton_toolbar)
            StatusBar.__init__(self, self.sceleton_statusbar)
            self.root.update()
            # self.covers_label[0].event_generate('<Button-1>')
        else:
            self.frame_empty_list = tk.Label(master=self.sceleton_services, text=msg)
            self.frame_empty_list.pack(fill=tk.BOTH, side=tk.TOP, expand=True)

    def left_listbox_onselect(self, evt):
        self.pause_len = 0
        self.pos_end = 0
        self.start = 0
        self.start_index = 0
        self.current_time = 0
        self.line_count = None
        self.stop()
        # self.pause()
        text = evt.widget.cget("text")
        for c in range(len(self.covers_label)):
            text1 = self.covers_label[c].cget("text")
            self.covers_label[c].configure(background="gray")
            if text1 == text:
                self.current_index = c
                self.covers_label[c].configure(background="blue")
        self.current_select = text
        self.current_dir = "data/" + text + "/"
        with open (self.current_dir + "rus.annot.txt", mode="r", encoding="UTF-8") as f:
            self.annotation = f.read() + "\n\n"
        with open (self.current_dir + "eng.annot.txt", mode="r", encoding="UTF-8") as f:
            self.annotation += f.read()

        with open(self.current_dir + "eng.sync.json", encoding="UTF-8", mode="r") as f:
            self.eng_sync = json.load(f)
        with open(self.current_dir + "rus.sync.json", encoding="UTF-8", mode="r") as f:
            self.rus_sync = json.load(f)

        # with open(self.current_dir + "orig.html", mode="r", encoding="UTF-8") as f:
        #     self.orig_html = f.read()
        # with open(self.current_dir + "rus.html", mode="r", encoding="UTF-8") as f:
        #     self.rus_html = f.read()
        # with open(self.current_dir + "eng.html", mode="r", encoding="UTF-8") as f:
        #     self.eng_html = f.read()
        with open(self.current_dir + "two.json", encoding="UTF-8", mode="r") as f:
            self.two = json.load(f)

        # with open(self.current_dir + "orig2.html", mode="r", encoding="UTF-8") as f:
        #     self.orig_html2 = f.read()
        # with open(self.current_dir + "rus2.html", mode="r", encoding="UTF-8") as f:
        #     self.rus_html2 = f.read()
        # with open(self.current_dir + "eng2.html", mode="r", encoding="UTF-8") as f:
        #     self.eng_html2 = f.read()
        # with open(self.current_dir + "two2.json", encoding="UTF-8", mode="r") as f:
        #     self.two2 = json.load(f)

        if not (self.frame_content1 is None):
            self.frame_content1.destroy()
        if not (self.frame_content2 is None):
            self.frame_content2.destroy()
        if not (self.right_cover_label is None):
            self.right_cover_label.destroy()
        if not (self.annotation_text_area1 is None):
            self.annotation_text_area1.destroy()
        if not (self.annotation_text_area2 is None):
            self.annotation_text_area2.destroy()
        if not (self.annotation_frame is None):
            self.annotation_frame.destroy()

        self.frame_content1 = tk.Frame(master=self.sceleton_table1)
        self.frame_content1.pack(fill=tk.Y, side=tk.TOP, expand=True, pady=0)

        self.frame_right_annotation1 = tk.Frame(self.frame_content1)
        self.frame_right_annotation1.pack(fill=tk.BOTH, side=tk.TOP, expand=True, pady=0)
        self.annotation_text_area1 = scrolledtext.ScrolledText(self.frame_right_annotation1,
                                                              wrap=tk.WORD,
                                                              font=("Arial", self.options["fontsize"]),
                                                              bg=self.options["bg"],
                                                              fg=self.options["fg"])
        self.annotation_text_area1.pack(fill=tk.BOTH, side=tk.RIGHT, expand=True, pady=5)
        # self.annotation_text_area1.insert(tk.END, self.annotation)
        self.annotation_text_area1.bind('<Button-1>', self.annotation_click)
        self.annotation_text_area1.delete(1.0, tk.END)
        # self.annotation_text_area1.bind("<Button-3>", self.left_popup)
        txt = open(self.current_dir + "eng.txt", mode="r", encoding="UTF-8")
        self.eng_book = txt.read()
        self.book = self.eng_book
        self.annotation_text_area1.insert(tk.END, self.eng_book)
        txt.close()
        self.annotation_text_area1.mark_set("insert", "1.0")
        self.annotation_text_area1.pack(fill=tk.BOTH, side=tk.RIGHT, expand=True, pady=5)
        self.annotation_frame = tk.Frame(master=self.sceleton_ads)
        self.annotation_frame.pack(fill=tk.BOTH, expand=True)
        self.annotation_text = scrolledtext.ScrolledText(master=self.annotation_frame, height=10, width=18,
                                                         wrap=tk.WORD,
                                                         font=("Consalos", 14))
        self.annotation_text.pack(fill=tk.BOTH, expand=True)
        self.annotation_text.insert(tk.END, self.annotation)
        self.annotation_text.tag_configure("center", justify='center')
        self.annotation_text.tag_add("center", 1.0, "end")
        self.annotation_text.configure(state='disabled')

        self.frame_content2 = tk.Frame(master=self.sceleton_table2)
        self.frame_content2.pack(fill=tk.Y, side=tk.TOP, expand=True, pady=0)

        self.frame_right_annotation2 = tk.Frame(self.frame_content2)
        self.frame_right_annotation2.pack(fill=tk.BOTH, side=tk.TOP, expand=True, pady=0)
        self.annotation_text_area2 = scrolledtext.ScrolledText(self.frame_right_annotation2,
                                                              wrap=tk.WORD,
                                                              font=("Arial", self.options["fontsize"]),
                                                              bg=self.options["bg"],
                                                              fg=self.options["fg"])
        self.annotation_text_area2.pack(fill=tk.BOTH, side=tk.RIGHT, expand=True, pady=5)
        # self.annotation_text_area2.insert(tk.END, self.annotation)
        self.annotation_text_area2.bind('<Button-1>', self.annotation_click)
        self.annotation_text_area2.delete(1.0, tk.END)
        # self.annotation_text_area2.bind("<Button-3>", self.left_popup)
        txt = open(self.current_dir + "rus.txt", mode="r", encoding="UTF-8")
        self.rus_book = txt.read()
        self.book_other = self.rus_book
        self.annotation_text_area2.insert(tk.END, self.rus_book)
        txt.close()
        self.annotation_text_area2.mark_set("insert", "1.0")

        self.frame_right_navigator.pack(fill=tk.X, side=tk.TOP, expand=False)

        if self.audio_lang.get() == self.english:
            pygame.mixer.music.load(self.current_dir + "eng.flac")
            self.annotation_text_area1.after_idle(self.annotation_text_area1.focus_set)
            self.annotation_text_area = self.annotation_text_area1
            self.annotation_text_area_other = self.annotation_text_area2
            self.sync = self.eng_sync
            self.book = self.eng_book
        else:
            pygame.mixer.music.load(self.current_dir + "rus.flac")
            self.annotation_text_area1.after_idle(self.annotation_text_area2.focus_set)
            self.annotation_text_area = self.annotation_text_area2
            self.annotation_text_area_other = self.annotation_text_area1
            self.sync = self.rus_sync
            self.book = self.rus_book

        self.loading = False
        # opt = self.options["positions"][self.current_select].split("\n")
        # if len(opt) == 3:
        #     self.pause_len = float(opt[0])
        #     self.annotation_text_area1.mark_set("insert", str(opt[1]))
        #     self.annotation_text_area1.see("insert")

    def annotation_click(self, event):
        if event.widget == self.annotation_text_area_other:
            self.root.update()
            if self.audio_lang.get() == self.english:
                self.audio_lang.set(self.russian)
                self.russian_click()
            else:
                self.audio_lang.set(self.english)
                self.english_click()
        index = self.annotation_text_area.index("current")
        ind = index.split(".")
        txt = self.book
        position = self.findnth(txt, "\n", int(ind[0]) - 2)
        for data in self.sync:
            if data[POS_START] >= position:
                count_lines = int(ind[0]) - 2
                count_chars = 0  # int(ind[1])
                self.annotation_text_area.mark_set("insert", f"{count_lines}.{count_chars}")
                # self.annotation_text_area.see("insert")
                self.centered_insert()
                self.pos_end = data[POS_START]
                self.start = data[TIME_START]
                self.pause_len = self.start * 1000

                self.scroll_other()
                break
        self.play()

    def scroll_other(self):
        if self.audio_lang.get() == self.english:
            curr = R_POS
            curr_other = L_POS
        else:
            curr = L_POS
            curr_other = R_POS

        for i in range(len(self.two)):
            if self.two[i][curr] > self.pos_end:
                txt = self.book_other[:self.two[i][curr_other]]
                split1 = txt.split("\n")
                count_lines = len(split1)
                count_chars = sum([len(j) + 1 for j in split1[-1].split(" ")]) - 1
                self.annotation_text_area_other.mark_set("insert", f"{count_lines}.{count_chars}")
                self.annotation_text_area_other.tag_add("start", f"1.0", f"{count_lines}.{count_chars}")
                self.annotation_text_area_other.tag_config("start", background="yellow", foreground="black")
                break

        self.centered_insert(center=True)
