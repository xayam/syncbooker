import os
import sys
from tkinter.messagebox import showinfo

from model.l18n import *
from model.utils import *

from controller.commands import Commands

from view.about import About
from view.options import Options
from view.catalog import Catalog


class Realization(Commands):

    def __init__(self, app):
        self.app = app

    def menu_service_language(self, event=None):
        if self.app.locale == event:
            return
        self.app.set_locale(event)
        self.app.options[LOCALE] = self.app.locale
        self.app.save_options()
        showinfo(MENU_SERVICE[self.app.locale], MENU_SERVICE_RESTART[self.app.locale])
        os.execv(sys.executable, [sys.executable, __file__] + sys.argv)

    def menu_file_quit_click(self, event=None):
        self.app.root.quit()
        self.app.root.destroy()
        self.app.root.update()

    def menu_help_faq_click(self, event=None):
        os.startfile(self.app.FAQ_HTML)

    def menu_help_updates_click(self, event=None):
        os.startfile(self.app.UPDATE_URL)

    def menu_help_about_click(self, event=None):
        About(app=self.app)

    def menu_service_catalog_click(self, event=None):
        Catalog(app=self.app)

    def menu_service_options_click(self, event=None):
        Options(app=self.app)
