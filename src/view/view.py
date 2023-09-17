import os
import tkinter as tk
import pygame
from tkinter import scrolledtext

from model.utils import *
from .sceleton import Sceleton


class View(Sceleton):

    def __init__(self, app):
        self.app = app
        self.root = tk.Tk()
        self.root.title(self.app.NAME + ' v' + self.app.VERSION)
        if os.path.exists(self.app.ICON_ICO):
            self.root.iconbitmap(self.app.ICON_ICO)
        self.root.geometry('1024x800')
        self.root.state('normal')

        pygame.mixer.pre_init()
        pygame.mixer.init()
        pygame.init()
        Sceleton.__init__(self, app=self)
        self.root.mainloop()

    def show_view(self):
        self.app.frame_content1 = tk.Frame(master=self.app.sceleton_table1)
        self.app.frame_content1.pack(fill=tk.BOTH, side=tk.TOP, expand=True, pady=0)

        self.app.frame_right_annotation1 = tk.Frame(self.app.frame_content1)
        self.app.frame_right_annotation1.pack(fill=tk.BOTH, side=tk.TOP, expand=True, pady=0)
        self.app.annotation_text_area1 = scrolledtext.ScrolledText(
            self.app.frame_right_annotation1,
            wrap=tk.WORD,
            font=(self.app.option[FONT], self.app.option[FONTSIZE]),
            bg=self.app.option[BG],
            fg=self.app.option[FG])
        self.app.annotation_text_area1.pack(fill=tk.BOTH, side=tk.RIGHT, expand=True, pady=5)
        # self.annotation_text_area1.insert(tk.END, self.annotation)
        self.app.annotation_text_area1.bind('<Button-1>', self.app.annotation_click)
        self.app.annotation_text_area1.delete(1.0, tk.END)
        # self.annotation_text_area1.bind("<Button-3>", self.left_popup)
        self.app.annotation_text_area1.insert(tk.END, self.app.eng_book)
        self.app.annotation_text_area1.mark_set("insert", "1.0")
        self.app.annotation_text_area1.pack(fill=tk.BOTH, side=tk.RIGHT, expand=True, pady=5)
        self.app.annotation_frame = tk.Frame(master=self.app.sceleton_ads)
        self.app.annotation_frame.pack(fill=tk.BOTH, expand=True)
        self.app.annotation_text = scrolledtext.ScrolledText(master=self.app.annotation_frame,
                                                             height=10, width=18,
                                                             wrap=tk.WORD,
                                                             font=("Consalos", 14))
        self.app.annotation_text.pack(fill=tk.BOTH, expand=True)
        self.app.annotation_text.insert(tk.END, self.app.annotation)
        self.app.annotation_text.tag_configure("center", justify='center')
        self.app.annotation_text.tag_add("center", 1.0, "end")
        self.app.annotation_text.configure(state='disabled')

        self.app.frame_content2 = tk.Frame(master=self.app.sceleton_table2)
        self.app.frame_content2.pack(fill=tk.BOTH, side=tk.TOP, expand=True, pady=0)

        self.app.frame_right_annotation2 = tk.Frame(self.app.frame_content2)
        self.app.frame_right_annotation2.pack(fill=tk.BOTH, side=tk.TOP, expand=True, pady=0)
        self.app.annotation_text_area2 = scrolledtext.ScrolledText(self.app.frame_right_annotation2,
                                                                   wrap=tk.WORD,
                                                                   font=(self.app.option[FONT],
                                                                         self.app.option[FONTSIZE]),
                                                                   bg=self.app.option[BG],
                                                                   fg=self.app.option[FG])
        self.app.annotation_text_area2.pack(fill=tk.BOTH, side=tk.RIGHT, expand=True, pady=5)
        # self.annotation_text_area2.insert(tk.END, self.annotation)
        self.app.annotation_text_area2.bind('<Button-1>', self.app.annotation_click)
        self.app.annotation_text_area2.delete(1.0, tk.END)
        # self.annotation_text_area2.bind("<Button-3>", self.left_popup)
        self.app.annotation_text_area2.insert(tk.END, self.app.rus_book)
        self.app.annotation_text_area2.mark_set("insert", "1.0")
        self.app.frame_right_navigator.pack(fill=tk.X, side=tk.TOP, expand=False)
