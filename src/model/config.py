import json
import os

from .utils import *
from .l18n import *


class Config:

    OPTIONS_JSON = "options.json"

    LICENSE = "../LICENSE"
    CASES_HTML = os.getcwd() + "/../cases.html"
    README_MD = os.getcwd() + "/../README.md"
    FAQ_HTML = os.getcwd() + "/../faq.html"
    DONATE = "https://yoomoney.ru/to/410014160363421"
    ICON_ICO = "../img/icon.ico"
    ICON_PNG = "../img/icon.png"

    GITHUB_SYNCBOOKER = "https://github.com/xayam/syncbooker"
    UPDATE_URL = "https://cloud.mail.ru/public/rdBB/KHvCjQdaT"
    SYNCBOOKER_CHAT = "https://t.me/syncbooker_chat"
    SYNCBOOKER_TELEGRAM = "@syncbooker_chat"
    EMAIL = "xayam@yandex.ru"

    RUS_ANNOT = "rus.annot.txt"
    ENG_ANNOT = "eng.annot.txt"
    RUS_SYNC = "rus.sync.json"
    ENG_SYNC = "eng.sync.json"
    MICRO_JSON = "micro.json"
    ENG_FB2 = "eng.fb2"
    RUS_FB2 = "rus.fb2"
    ENG_TXT = "eng.txt"
    RUS_TXT = "rus.txt"
    ENG_FLAC = "eng.flac"
    RUS_FLAC = "rus.flac"
    COVER = "cover.jpg"
    VALID = "valid"

    RUS_ORIG = "rus.orig.html"
    ENG_ORIG = "eng.orig.html"

    BOOK_SCHEME = [
        RUS_ANNOT, ENG_ANNOT, RUS_SYNC,
        ENG_SYNC, MICRO_JSON, ENG_FB2,
        RUS_FB2, ENG_TXT, RUS_TXT,
        ENG_FLAC, RUS_FLAC, COVER, VALID
    ]

    def __init__(self, app=None):
        self.app = app
        self.locale = EN
        self.books = []
        self.options = {LOCALE: EN,
                        FG: "black",
                        BG: "white",
                        SEL: "yellow",
                        FONT: "Arial",
                        FONTSIZE: 20,
                        POSITIONS: {i: {POSI: "0.0\n0.0\n0.0", AUDIO: EN} for i in self.books}
                        }
        self.load_options()
        self.save_options()
        self.set_locale(self.options[LOCALE])

    def set_locale(self, locale):
        self.locale = locale

    def load_options(self):
        if os.path.exists(self.OPTIONS_JSON):
            with open(self.OPTIONS_JSON, mode="r") as opt:
                self.options = json.load(opt)

    def save_options(self):
        json_string = json.dumps(self.options)
        with open(self.OPTIONS_JSON, mode="w") as opt:
            opt.write(json_string)
