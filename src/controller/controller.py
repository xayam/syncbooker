from tkinter import font
from model.utils import *
from model.l18n import *


class Controller:

    def __init__(self, app):
        self.app = app
        self.loading = True
        self.pause_len = 0
        self.pos_end = 0
        self.pos_end_other = 0
        self.sync_i = 0
        self.sync_other_i = 0
        self.start = 0
        self.start_index = 0
        self.current_time = 0
        self.line_count = None
        self.current_select = ''
        self.current_dir = ''
        self.current_index = None

    def left_listbox_onselect(self, evt):
        self.pause_len = 0
        self.pos_end = 0
        self.pos_end_other = 0
        self.sync_i = 0
        self.sync_other_i = 0
        self.start = 0
        self.start_index = 0
        self.current_time = 0
        self.line_count = None
        self.app.stop()
        text = evt.widget.cget("text")
        for c in range(len(self.app.covers_label)):
            text1 = self.app.covers_label[c].cget("text")
            self.app.covers_label[c].configure(background="gray")
            if text1 == text:
                self.current_index = c
                self.app.covers_label[c].configure(background="blue")
        self.current_select = text
        self.current_dir = "../data/" + text + "/"

        self.pause_len = float(self.app.options[POSITIONS][self.current_select][POSI].split("\n")[0])

        self.app.pre_load()
        self.app.show_view()

        self.loading = False

        self.app.music_load()

    def annotation_click(self, event):
        index = self.app.annotation_text_area.index("current")
        txt = self.app.book
        if event.widget == self.app.annotation_text_area_other:
            index = self.app.annotation_text_area_other.index("current")
            txt = self.app.book_other
            self.app.root.update()
            if self.app.options[POSITIONS][self.app.current_select][AUDIO] == EN:
                self.app.options[POSITIONS][self.app.current_select][AUDIO] = RU
                self.app.russian_click()
            else:
                self.app.options[POSITIONS][self.app.current_select][AUDIO] = EN
                self.app.english_click()
        if self.app.options[POSITIONS][self.app.current_select][AUDIO] == EN:
            curr = R_POS
            curr_other = L_POS
            self.app.sync_other = self.app.rus_sync
        else:
            curr = L_POS
            curr_other = R_POS
            self.app.sync_other = self.app.eng_sync
        ind = index.split(".")
        position = findnth(txt, "\n", int(ind[0]) - 2)
        for i in range(len(self.app.micro)):
            for j in range(len(self.app.micro[i])):
                if self.app.micro[i][j][curr] >= position:
                    count_lines = int(ind[0]) - 2
                    count_chars = 0  # int(ind[1])
                    self.app.annotation_text_area.mark_set("insert", f"{count_lines}.{count_chars}")
                    self.centered_insert()
                    self.pos_end = self.app.micro[i][j][curr]
                    self.pos_end_other = self.app.micro[i][j][curr_other]
                    for data in self.app.sync:
                        if data[POS_START] >= position:
                            self.start = data[TIME_START]
                            break
                    self.pause_len = self.start * 1000
                    self.scroll_other()
                    self.app.play()
                    return

    def scroll_other(self):
        txt = self.app.book_other[:self.pos_end_other]
        split1 = txt.split("\n")
        words = split1[-1].split(" ")
        count_chars = 0
        for j in range(len(words) - 1):
            count_chars += len(words[j]) + 1
            try:
                if (self.app.sync_other[self.sync_other_i][WORD].lower() == words[j].lower()) and \
                        (len(words[j]) > 2) and \
                        (self.app.sync_other[self.sync_other_i + 1][WORD].lower() == words[j + 1].lower()) and \
                        (len(words[j + 1]) > 2):
                    break
            except IndexError:
                break
        count_lines = len(split1)
        self.app.annotation_text_area_other.mark_set("insert", f"{count_lines}.{count_chars}")
        self.app.annotation_text_area_other.tag_remove("start", "1.0", "end")
        self.app.annotation_text_area_other.tag_add("start", f"1.0", f"{count_lines}.{count_chars}")
        self.app.annotation_text_area_other.tag_config("start",
                                                       background=self.app.options[SEL],
                                                       foreground=self.app.options[FG])
        self.centered_insert(center=True)

    def centered_insert(self, center=False):
        if self.line_count is None:
            self.text_area_line_count(center)
        if center:
            center = self.app.annotation_text_area_other
        else:
            center = self.app.annotation_text_area
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
            center = self.app.annotation_text_area_other
            book = self.app.book_other
        else:
            center = self.app.annotation_text_area
            book = self.app.book
        font1 = font.Font(font=center['font'])
        widget_width = center.winfo_width()
        max_chars_per_line = int(widget_width / font1.measure(" "))
        lines = book.split("\n\n")
        count = -2
        for i in lines:
            count += 3 + len(i) // max_chars_per_line
        self.line_count = count
