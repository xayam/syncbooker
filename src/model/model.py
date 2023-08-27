import json
import pygame

from .l18n import *
from .utils import *
from .config import Config


class Model(Config):

    def __init__(self, app):
        self.app = app
        Config.__init__(self, app=self)

    def pre_load(self):
        with open(self.app.current_dir + self.RUS_ANNOT, mode="r", encoding="UTF-8") as f:
            self.app.annotation = f.read() + "\n\n"
        with open(self.app.current_dir + self.ENG_ANNOT, mode="r", encoding="UTF-8") as f:
            self.app.annotation += f.read()

        with open(self.app.current_dir + self.ENG_SYNC, encoding="UTF-8", mode="r") as f:
            self.app.eng_sync = json.load(f)
        with open(self.app.current_dir + self.RUS_SYNC, encoding="UTF-8", mode="r") as f:
            self.app.rus_sync = json.load(f)

        with open(self.app.current_dir + self.MICRO_JSON, encoding="UTF-8", mode="r") as f:
            self.app.micro = json.load(f)

        if not (self.app.frame_content1 is None):
            self.app.frame_content1.destroy()
        if not (self.app.frame_content2 is None):
            self.app.frame_content2.destroy()
        if not (self.app.right_cover_label is None):
            self.app.right_cover_label.destroy()
        if not (self.app.annotation_text_area1 is None):
            self.app.annotation_text_area1.destroy()
        if not (self.app.annotation_text_area2 is None):
            self.app.annotation_text_area2.destroy()
        if not (self.app.annotation_frame is None):
            self.app.annotation_frame.destroy()

        with open(self.app.current_dir + self.ENG_TXT, mode="r", encoding="UTF-8") as txt:
            self.app.eng_book = txt.read()
            self.app.book = self.app.eng_book
        with open(self.app.current_dir + self.RUS_TXT, mode="r", encoding="UTF-8") as txt:
            self.app.rus_book = txt.read()
            self.app.book_other = self.app.rus_book

    def music_load(self):
        if self.app.options[POSITIONS][self.app.current_select][AUDIO] == EN:
            pygame.mixer.music.load(self.app.current_dir + self.app.ENG_FLAC)
            self.app.annotation_text_area1.after_idle(self.app.annotation_text_area1.focus_set)
            self.app.annotation_text_area = self.app.annotation_text_area1
            self.app.annotation_text_area_other = self.app.annotation_text_area2
            self.app.sync = self.app.eng_sync
            self.app.book = self.app.eng_book
        else:
            pygame.mixer.music.load(self.app.current_dir + self.app.RUS_FLAC)
            self.app.annotation_text_area1.after_idle(self.app.annotation_text_area2.focus_set)
            self.app.annotation_text_area = self.app.annotation_text_area2
            self.app.annotation_text_area_other = self.app.annotation_text_area1
            self.app.sync = self.app.rus_sync
            self.app.book = self.app.rus_book
        self.app.statusbar_label1.configure(
            text=STATUS_AUDIO[self.app.locale] + ": " +
            self.app.options[POSITIONS][self.app.current_select][AUDIO])
        self.app.root.update()
        self.app.play()
