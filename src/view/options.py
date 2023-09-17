import os
import tkinter as tk
from tkinter import ttk, font
from tkinter.colorchooser import askcolor
# from tkinter import scrolledtext
# from tkinter import font
# from PIL import ImageTk, Image

from model.l18n import *
from model.utils import *


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

    def show_options(self):
        self.options.grab_set()
        self.options.mainloop()

    def options_color_click(self, entry, button):
        result = askcolor(title=OPTIONS_COLOR_SELECTION[self.app.locale])
        if not (result[1] is None):
            entry.delete(0, tk.END)
            entry.insert(0, str(result[1]))
            button["bg"] = str(result[1])
            button["fg"] = color_contrast(str(result[1])),

    def options_font_click(self, event):
        w = event.widget
        try:
            index = int(w.curselection()[0])
            value = w.get(index)
            self.options_font_variable.set(value)
        except IndexError:
            pass
        self.options_font_absde["font"] = (self.options_font_entry.get(), int(self.options_fontsize_entry.get()))

    def options_fontsizes_click(self, event):
        w = event.widget
        try:
            index = int(w.curselection()[0])
            value = w.get(index)
            self.options_fontsize_variable.set(value)
        except IndexError:
            pass
        self.options_font_absde["font"] = (self.options_font_entry.get(), int(self.options_fontsize_entry.get()))

    def options_button_save_click(self):
        self.app.option[FG] = self.options_fg_entry.get()
        self.app.option[BG] = self.options_bg_entry.get()
        self.app.option[SEL] = self.options_sel_entry.get()
        self.app.option[FONT] = self.options_font_entry.get()
        try:
            self.app.option[FONTSIZE] = int(self.options_fontsize_entry.get())
        except ValueError:
            self.app.option[FONTSIZE] = 20
            self.options_fontsize_entry.delete(0, tk.END)
            self.options_fontsize_entry.insert(0, str(self.app.option[FONTSIZE]))
        self.app.save_options()
        if not (self.app.annotation_text_area1 is None):
            self.app.annotation_text_area1[FG] = self.app.option[FG]
            self.app.annotation_text_area1[BG] = self.app.option[BG]
            self.app.annotation_text_area1[FONT] = (self.app.option[FONT], self.app.option[FONTSIZE])
        if not (self.app.annotation_text_area2 is None):
            self.app.annotation_text_area2[FG] = self.app.option[FG]
            self.app.annotation_text_area2[BG] = self.app.option[BG]
            self.app.annotation_text_area2[FONT] = (self.app.option[FONT], self.app.option[FONTSIZE])
        self.options.destroy()

    def _create_options(self):
        self.options_tabs = ttk.Notebook(self.options)
        self.options_tabs.pack(fill=tk.BOTH, expand=True, pady=5)
        self.options_tab_color = tk.Frame(self.options_tabs)
        self.options_tab_color.pack(fill=tk.BOTH, expand=True)
        self.options_tab_font1 = tk.Frame(self.options_tabs)
        self.options_tab_font1.pack(fill=tk.BOTH, expand=True)
        self.options_tabs.add(self.options_tab_color, text=OPTIONS_COLOR[self.app.locale])
        self.options_tabs.add(self.options_tab_font1, text=OPTIONS_FONT[self.app.locale])

        self.options_frame_result = tk.Frame(self.options, padx=10, pady=10)
        self.options_frame_result.pack(fill=tk.X, expand=True)
        self.options_button_save = tk.Button(self.options, text="Сохранить", padx=5,
                                             command=self.options_button_save_click)
        self.options_button_save.pack(side=tk.RIGHT, padx=10, pady=10)

        self.options_fg_label = tk.Label(self.options_tab_color, text=OPTIONS_COLOR_FG[self.app.locale])
        self.options_fg_label.grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.options_fg_entry = tk.Entry(self.options_tab_color)
        self.options_fg_entry.grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)
        self.options_fg_entry.insert(0, self.app.option[FG])
        self.options_fg_button = tk.Button(self.options_tab_color, text="...", padx=10,
                                           bg=self.app.option[FG],
                                           fg=color_contrast(self.app.option[FG]),
                                           command=lambda: self.options_color_click(self.options_fg_entry,
                                                                                    self.options_fg_button))
        self.options_fg_button.grid(row=0, column=2, sticky=tk.W)

        self.options_bg_label = tk.Label(self.options_tab_color, text=OPTIONS_COLOR_BG[self.app.locale])
        self.options_bg_label.grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.options_bg_entry = tk.Entry(self.options_tab_color)
        self.options_bg_entry.grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)
        self.options_bg_entry.insert(0, self.app.option[BG])
        self.options_bg_button = tk.Button(self.options_tab_color, text="...", padx=10,
                                           bg=self.app.option[BG],
                                           fg=color_contrast(self.app.option[BG]),
                                           command=lambda: self.options_color_click(self.options_bg_entry,
                                                                                    self.options_bg_button))
        self.options_bg_button.grid(row=1, column=2, sticky=tk.W)

        self.options_sel_label = tk.Label(self.options_tab_color, text=OPTIONS_COLOR_SEL[self.app.locale])
        self.options_sel_label.grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        self.options_sel_entry = tk.Entry(self.options_tab_color)
        self.options_sel_entry.grid(row=2, column=1, sticky=tk.W, padx=5, pady=5)
        self.options_sel_entry.insert(0, self.app.option[SEL])
        self.options_sel_button = tk.Button(self.options_tab_color, text="...", padx=10,
                                            bg=self.app.option[SEL],
                                            fg=color_contrast(self.app.option[SEL]),
                                            command=lambda: self.options_color_click(self.options_sel_entry,
                                                                                     self.options_sel_button))
        self.options_sel_button.grid(row=2, column=2, sticky=tk.W)

        self.options_tab_font = tk.Frame(self.options_tab_font1)
        self.options_tab_font.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.options_font_absde = tk.Label(self.options_tab_font1, text="Abcde Абвгде", height=1,
                                           font=(self.app.option[FONT], self.app.option[FONTSIZE]))
        self.options_font_absde.pack(fill=tk.X, expand=True, padx=5, pady=5)

        self.options_font_variable = tk.StringVar()
        self.options_font_variable.set(self.app.option[FONT])
        self.options_font_entry = tk.Entry(self.options_tab_font,
                                           textvariable=self.options_font_variable,
                                           state="disabled")
        self.options_font_entry.grid(row=0, column=0, sticky=tk.NSEW, padx=5, pady=5)

        self.options_fontsize_variable = tk.StringVar()
        self.options_fontsize_variable.set(self.app.option[FONTSIZE])
        self.options_fontsize_entry = tk.Entry(self.options_tab_font,
                                               textvariable=self.options_fontsize_variable,
                                               state="disabled")
        self.options_fontsize_entry.grid(row=0, column=1, sticky=tk.NSEW, padx=5, pady=5)

        self.fonts = font.families()
        self.fonts_var = tk.Variable(value=self.fonts)
        self.fonts_frame = tk.Frame(self.options_tab_font)
        self.fonts_scrollbar = tk.Scrollbar(self.fonts_frame, orient=tk.VERTICAL)
        self.options_fonts_listbox = tk.Listbox(self.fonts_frame,
                                                listvariable=self.fonts_var,
                                                yscrollcommand=self.fonts_scrollbar.set)
        self.fonts_scrollbar.config(command=self.options_fonts_listbox.yview)
        self.fonts_scrollbar.pack(fill=tk.Y, side=tk.RIGHT)
        self.options_fonts_listbox.pack(fill=tk.BOTH, expand=True)
        self.options_fonts_listbox.bind('<<ListboxSelect>>', self.options_font_click)
        self.fonts_frame.grid(row=1, column=0, sticky=tk.NSEW, padx=5, pady=5)
        i = 0
        for f in self.fonts:
            if f == self.app.option[FONT]:
                self.options_fonts_listbox.see(i)
                break
            i += 1

        self.fontsizes = [i for i in range(6, 52, 2)]
        self.fontsizes_var = tk.Variable(value=self.fontsizes)
        self.fontsizes_frame = tk.Frame(self.options_tab_font)
        self.fontsizes_scrollbar = tk.Scrollbar(self.fontsizes_frame, orient=tk.VERTICAL)
        self.options_fontsizes_listbox = tk.Listbox(self.fontsizes_frame,
                                                listvariable=self.fontsizes_var,
                                                yscrollcommand=self.fontsizes_scrollbar.set)
        self.fontsizes_scrollbar.config(command=self.options_fontsizes_listbox.yview)
        self.fontsizes_scrollbar.pack(fill=tk.Y, side=tk.RIGHT)
        self.options_fontsizes_listbox.pack(fill=tk.BOTH, expand=True)
        self.options_fontsizes_listbox.bind('<<ListboxSelect>>', self.options_fontsizes_click)
        self.fontsizes_frame.grid(row=1, column=1, sticky=tk.NSEW, padx=5, pady=5)
        i = 0
        for f in self.fontsizes:
            if f == self.app.option[FONTSIZE]:
                self.options_fontsizes_listbox.see(i)
                break
            i += 1

        self.options_tab_font.grid_columnconfigure(0, weight=1, uniform="group2")
        self.options_tab_font.grid_columnconfigure(1, weight=1, uniform="group2")
