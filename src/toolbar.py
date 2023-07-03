import pickle
import tkinter as tk
import pygame
from commands import Commands
from tkinter import ttk, font
from consts import *


class ToolBar(Commands):

    def __init__(self, root, toolbar: tk.Frame):
        self.root = root
        self.toolbar = toolbar

        self.pause_len = 0
        self._create_toolbar()

    def _create_toolbar(self):
        # self.toolbar_options_click = tk.Button(master=self.toolbar,
        #                                        text="Настройки", width=15, relief=tk.FLAT,
        #                                        command=self.toolbar_options_click)
        # self.toolbar_options_click.pack(fill=tk.X, side=tk.LEFT, expand=False)



        self.frame_right_navigator = tk.Frame(self.toolbar)

        empty1 = tk.Label(master=self.frame_right_navigator, text="", font=("Aerial", 20), width=1)
        empty1.pack(fill=tk.BOTH, side=tk.LEFT, expand=False)

        # self.bg_color_button = tk.Button(master=self.frame_right_navigator,
        #                                    text=u"🔲",
        #                                    font=("Aerial", 20),
        #                                    # command=self.
        #                                  )
        # self.bg_color_button.pack(fill=tk.BOTH, side=tk.LEFT, expand=False)
        #
        # self.font_color_button = tk.Button(master=self.frame_right_navigator,
        #                                    text=u"◑",
        #                                    font=("Aerial", 20),
        #                                    # command=self.
        #                                  )
        # self.font_color_button.pack(fill=tk.BOTH, side=tk.LEFT, expand=False)
        #
        # self.size_font_button = tk.Button(master=self.frame_right_navigator,
        #                                   text=u"🗚",
        #                                   font=("Aerial", 20),
        #                                   # command=self.
        #                                  )
        # self.size_font_button.pack(fill=tk.BOTH, side=tk.LEFT, expand=False)

        empty2 = tk.Label(master=self.frame_right_navigator, text="", font=("Aerial", 20), width=14)
        empty2.pack(fill=tk.BOTH, side=tk.LEFT, expand=False)

        # self.label_audio = ttk.Label(master=self.frame_right_navigator, font=("Aerial", 20), text=u"🕫")
        # self.label_audio.pack(fill=tk.BOTH, side=tk.LEFT, expand=False)

        position = {"padx": 0, "pady": 0, "anchor": tk.NW}
        # self.btn_english = ttk.Radiobutton(master=self.frame_right_navigator, text=self.english,
        #                                    value=self.english, variable=self.audio_lang, command=self.english_click)
        # self.btn_english.pack(fill=tk.BOTH, side=tk.LEFT, expand=False, **position)
        # self.btn_russian = ttk.Radiobutton(master=self.frame_right_navigator, text=self.russian,
        #                              value=self.russian, variable=self.audio_lang, command=self.russian_click)
        # self.btn_russian.pack(fill=tk.BOTH, side=tk.LEFT, expand=False, **position)

        empty3 = tk.Label(master=self.frame_right_navigator, text="", font=("Aerial", 20), width=1)
        empty3.pack(fill=tk.BOTH, side=tk.LEFT, expand=False)

        self.backward_button = tk.Button(master=self.frame_right_navigator,
                                         text=u"\u23ee",
                                         font=("Aerial", 20),
                                         command=self.backward
                                         )
        self.backward_button.pack(fill=tk.BOTH, side=tk.LEFT, expand=False)
        self.play_button = tk.Button(master=self.frame_right_navigator,
                                     text=u"\u23f5",
                                     font=("Aerial", 20),
                                     command=self.play
                                     )
        self.play_button.pack(fill=tk.BOTH, side=tk.LEFT, expand=False)
        self.pause_button = tk.Button(master=self.frame_right_navigator,
                                      text=u"\u23f8",
                                      font=("Aerial", 20),
                                      command=self.pause
                                      )
        self.pause_button.pack(fill=tk.BOTH, side=tk.LEFT, expand=False)
        self.stop_button = tk.Button(master=self.frame_right_navigator,
                                     text=u"\u23f9",
                                     font=("Aerial", 20),
                                     command=self.stop
                                     )
        self.stop_button.pack(fill=tk.BOTH, side=tk.LEFT, expand=False)
        self.forward_button = tk.Button(master=self.frame_right_navigator,
                                        text=u"\u23ed",
                                        font=("Aerial", 20),
                                        command=self.forward
                                        )
        self.forward_button.pack(fill=tk.BOTH, side=tk.LEFT, expand=False)

        self.label_language_audio = ttk.Label(master=self.frame_right_navigator, textvariable=self.audio_lang)
        # self.label_language_audio.pack(fill=tk.BOTH, side=tk.LEFT, expand=False, **position)

    def russian_click(self):
        self.pause()
        self.statusbar_label1.configure(text="Audio: " + self.audio_lang.get())
        self.annotation_text_area1.tag_remove("start", "1.0", "end")
        self.annotation_text_area2.tag_remove("start", "1.0", "end")
        pygame.mixer.music.load(self.current_dir + "rus.flac")
        self.annotation_text_area2.after_idle(self.annotation_text_area2.focus_set)
        self.play()

    def english_click(self):
        self.pause()
        self.statusbar_label1.configure(text="Audio: " + self.audio_lang.get())
        self.annotation_text_area1.tag_remove("start", "1.0", "end")
        self.annotation_text_area2.tag_remove("start", "1.0", "end")
        pygame.mixer.music.load(self.current_dir + "eng.flac")
        self.annotation_text_area1.after_idle(self.annotation_text_area1.focus_set)
        self.play()

    def backward(self):
        if self.books:
            self.annotation_text_area1.tag_remove("start", "1.0", "end")
            self.annotation_text_area2.tag_remove("start", "1.0", "end")
            # self.frame_left_list.selection_clear(0, 'end')
            index = self.current_index - 1
            if index < 0:
                index = len(self.covers_label) - 1
            self.root.update()
            self.covers_label[index].event_generate("<Button-1>")

    def play(self):
        self.flag_pause = False
        pygame.mixer.music.play(loops=0, start=self.pause_len / 1000.0)
        # pygame.mixer.music.set_pos(self.start)
        self.play_timer()

    def pause(self):
        self.flag_pause = True
        pygame.mixer.music.pause()
        self.pause_len += pygame.mixer.music.get_pos()

    def stop(self):
        if not self.loading:
            self.annotation_text_area.tag_remove("insert", "1.0", "end")
            self.annotation_text_area1.tag_remove("start", "1.0", "end")
            self.annotation_text_area2.tag_remove("start", "1.0", "end")
        pygame.mixer.music.stop()
        self.flag_pause = True
        self.pause_len = 0
        self.pos_end = 0
        self.start = 0
        if not self.loading:
            self.annotation_text_area_other.focus()
            self.annotation_text_area_other.mark_set("insert", "1.0")
            self.annotation_text_area_other.see("insert")
            self.annotation_text_area.focus()
            self.annotation_text_area.mark_set("insert", "1.0")
            self.annotation_text_area.see("insert")

    def forward(self):
        if self.books:
            self.annotation_text_area1.tag_remove("start", "1.0", "end")
            self.annotation_text_area2.tag_remove("start", "1.0", "end")
            # self.frame_left_list.selection_clear(0, 'end')
            index = self.current_index + 1
            if index > len(self.covers_label) - 1:
                index = 0
            self.root.update()
            self.covers_label[index].event_generate('<Button-1>')

    def play_timer(self):
        if self.flag_pause:
            return
        self.annotation_text_area1.tag_remove("start", "1.0", "end")
        self.annotation_text_area2.tag_remove("start", "1.0", "end")
        if self.audio_lang.get() == self.english:
            self.annotation_text_area = self.annotation_text_area1
            self.sync = self.eng_sync
            self.book = self.eng_book
            self.annotation_text_area_other = self.annotation_text_area2
            self.sync_other = self.rus_sync
            self.book_other = self.rus_book
        else:
            self.annotation_text_area = self.annotation_text_area2
            self.sync = self.rus_sync
            self.book = self.rus_book
            self.annotation_text_area_other = self.annotation_text_area1
            self.sync_other = self.eng_sync
            self.book_other = self.eng_book

        for i in range(len(self.sync) - 1):
            if self.sync[i][TIME_START] * 1000.0 > self.pause_len + pygame.mixer.music.get_pos():
                txt = self.book[:self.sync[i][POS_START]]
                split1 = txt.split("\n")
                words = split1[-1].split(" ")
                count_chars = 0
                for j in range(len(words) - 1):
                    count_chars += len(words[j]) + 1
                    if (self.sync[i][WORD].lower() == words[j].lower()) and (len(words[j]) > 2) and \
                            (self.sync[i + 1][WORD].lower() == words[j + 1].lower()) and (len(words[j + 1]) > 2):
                        break
                count_lines = len(split1)
                # self.annotation_text_area.mark_set("insert", f"{count_lines}.{5} lineend")
                self.annotation_text_area.mark_set("insert", f"{count_lines}.{count_chars}")
                self.annotation_text_area.tag_add("start", f"1.0", f"{count_lines}.{count_chars}")
                self.annotation_text_area.tag_config("start", background="yellow", foreground="black")
                if self.flag_pause:
                    self.annotation_text_area.see("insert")
                self.centered_insert()
                self.pos_end = self.sync[i][POS_START]
                self.sync_i = i
                self.start = self.sync[i][TIME_START]

                self.scroll_other()

                # with open("options.pkl", mode="wb") as pkl:
                #     self.options["positions"][self.current_select] = \
                #         str(self.pause_len + pygame.mixer.music.get_pos()) + \
                #         "\n" + f"{count_lines}.{count_chars}" + \
                #         "\n" + str(self.start)
                #     pickle.dump(self.options, pkl)
                break
                
        self.statusbar_label2.configure(text="Position: " +
                                             self.annotation_text_area1.index("current") + "/" +
                                             self.annotation_text_area2.index("current"))
        if not self.flag_pause:
            self.root.after(500, self.play_timer)

    def centered_insert(self, center=False):
        if self.line_count is None:
            self.text_area_line_count(center)
        if center:
            center = self.annotation_text_area_other
        else:
            center = self.annotation_text_area
        center.see("insert")
        height = int(center['height'])
        w_height = center.winfo_height()
        height_1 = w_height / height
        top_y, _ = center.yview()

        if top_y:
            if center.bbox("insert") is not None:
                cursor_y = center.bbox("insert")[1] / height_1
                center_y = top_y
                if cursor_y > height / 2:
                    center_y = top_y + (cursor_y - height / 2) / self.line_count
                center.yview_moveto(center_y)

    def text_area_line_count(self, center=False):
        if center:
            center = self.annotation_text_area_other
            book = self.book_other
        else:
            center = self.annotation_text_area
            book = self.book
        font1 = font.Font(font=center['font'])
        widget_width = center.winfo_width()
        max_chars_per_line = int(widget_width / font1.measure(" "))
        lines = book.split("\n\n")
        count = -2
        for l in lines:
            count += 3 + len(l) // max_chars_per_line
        self.line_count = count

    def findnth(self, string, substring, n):
        parts = string.split(substring, n + 1)
        if len(parts) <= n + 1:
            return -1
        return len(string) - len(parts[-1]) - len(substring)
