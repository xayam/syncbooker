import pygame

from model.utils import *
from model.l18n import *


class Player:

    def __init__(self, app):
        self.app = app

    def backward(self):
        if self.app.books:
            self.app.annotation_text_area1.tag_remove("start", "1.0", "end")
            self.app.annotation_text_area2.tag_remove("start", "1.0", "end")
            index = self.app.current_index - 1
            if index < 0:
                index = len(self.app.covers_label) - 1
            self.app.root.update()
            self.app.covers_label[index].event_generate("<Button-1>")

    def play(self):
        self.app.flag_pause = False
        pygame.mixer.music.play(loops=0, start=self.app.pause_len / 1000.0)
        self.app.play_timer()

    def pause(self):
        self.app.flag_pause = True
        pygame.mixer.music.pause()
        self.app.pause_len += pygame.mixer.music.get_pos()

    def stop(self):
        if not self.app.loading:
            self.app.annotation_text_area.tag_remove("insert", "1.0", "end")
            self.app.annotation_text_area1.tag_remove("start", "1.0", "end")
            self.app.annotation_text_area2.tag_remove("start", "1.0", "end")
        pygame.mixer.music.stop()
        self.app.flag_pause = True
        self.app.pause_len = 0
        self.app.pos_end = 0
        self.app.start = 0
        if not self.app.loading:
            self.app.annotation_text_area_other.focus()
            self.app.annotation_text_area_other.mark_set("insert", "1.0")
            self.app.annotation_text_area_other.see("insert")
            self.app.annotation_text_area.focus()
            self.app.annotation_text_area.mark_set("insert", "1.0")
            self.app.annotation_text_area.see("insert")

    def forward(self):
        if self.app.books:
            self.app.annotation_text_area1.tag_remove("start", "1.0", "end")
            self.app.annotation_text_area2.tag_remove("start", "1.0", "end")
            index = self.app.current_index + 1
            if index > len(self.app.covers_label) - 1:
                index = 0
            self.app.root.update()
            self.app.covers_label[index].event_generate('<Button-1>')

    def russian_click(self):
        self.language_click(textarea=self.app.annotation_text_area2,
                            flac=self.app.current_dir + self.app.RUS_FLAC)

    def english_click(self):
        self.language_click(textarea=self.app.annotation_text_area1,
                            flac=self.app.current_dir + self.app.ENG_FLAC)

    def language_click(self, textarea, flac):
        self.app.pause()
        self.app.statusbar_label1.configure(
            text=STATUS_AUDIO[self.app.locale] + ": " +
            self.app.option[POSITIONS][self.app.current_select][AUDIO])
        self.app.annotation_text_area1.tag_remove("start", "1.0", "end")
        self.app.annotation_text_area2.tag_remove("start", "1.0", "end")
        pygame.mixer.music.load(flac)
        textarea.after_idle(textarea.focus_set)
        self.app.play()

    def play_timer(self):
        if self.app.flag_pause:
            return
        self.app.annotation_text_area1.tag_remove("start", "1.0", "end")
        self.app.annotation_text_area2.tag_remove("start", "1.0", "end")
        if self.app.option[POSITIONS][self.app.current_select][AUDIO] == EN:
            curr = R_POS
            curr_other = L_POS
            self.app.annotation_text_area = self.app.annotation_text_area1
            self.app.sync = self.app.eng_sync
            self.app.book = self.app.eng_book
            self.app.annotation_text_area_other = self.app.annotation_text_area2
            self.app.sync_other = self.app.rus_sync
            self.app.book_other = self.app.rus_book
        else:
            curr = L_POS
            curr_other = R_POS
            self.app.annotation_text_area = self.app.annotation_text_area2
            self.app.sync = self.app.rus_sync
            self.app.book = self.app.rus_book
            self.app.annotation_text_area_other = self.app.annotation_text_area1
            self.app.sync_other = self.app.eng_sync
            self.app.book_other = self.app.eng_book

        for i in range(len(self.app.sync) - 1):
            if self.app.sync[i][TIME_START] * 1000.0 > self.app.pause_len + pygame.mixer.music.get_pos():
                txt = self.app.book[:self.app.sync[i][POS_START]]
                split1 = txt.split("\n")
                words = split1[-1].split(" ")
                count_chars = 0
                for j in range(len(words) - 1):
                    count_chars += len(words[j]) + 1
                    if (self.app.sync[i][WORD].lower() == words[j].lower()) and (len(words[j]) > 2) and \
                            (self.app.sync[i + 1][WORD].lower() == words[j + 1].lower()) and (len(words[j + 1]) > 2):
                        break
                count_lines = len(split1)
                # self.annotation_text_area.mark_set("insert", f"{count_lines}.{5} lineend")
                self.app.annotation_text_area.mark_set("insert", f"{count_lines}.{count_chars}")
                self.app.annotation_text_area.tag_add("start", f"1.0", f"{count_lines}.{count_chars}")
                self.app.annotation_text_area.tag_config("start",
                                                         background=self.app.option[SEL],
                                                         foreground=self.app.option[FG])
                if self.app.flag_pause:
                    self.app.annotation_text_area.see("insert")
                self.app.centered_insert()
                for k in range(len(self.app.micro)):
                    for j in range(len(self.app.micro[k])):
                        if self.app.micro[k][j][curr] >= self.app.sync[i][POS_START]:
                            for z in range(len(self.app.sync_other) - 1):
                                if self.app.micro[k][j][curr_other] >= self.app.sync_other[z][POS_START]:
                                    self.app.pos_end = self.app.micro[k][j][curr]
                                    self.app.sync_i = i
                                    self.app.pos_end_other = self.app.micro[k][j][curr_other]
                                    self.app.sync_other_i = z
                                    self.app.start = self.app.sync[i][TIME_START]
                                    self.app.scroll_other()

                                    self.app.statusbar_label2.configure(
                                        text=STATUS_POSITION[self.app.locale] + ": " +
                                        self.app.annotation_text_area1.index("current") + "/" +
                                        self.app.annotation_text_area2.index("current"))
                                    self.app.option[POSITIONS][self.app.current_select][POSI] = \
                                        str(self.app.pause_len + pygame.mixer.music.get_pos()) + \
                                        "\n" + f"{count_lines}.{count_chars}" + \
                                        "\n" + str(self.app.start)
                                    self.app.save_options()
                                    if not self.app.flag_pause:
                                        self.app.root.after(500, self.play_timer)
                                    return
