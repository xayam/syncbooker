import tkinter as tk
from sceleton import Sceleton
import pygame


class App(Sceleton):
    NAME = 'SyncBooker'
    VERSION = '2.1'

    def __init__(self):

        self.root = tk.Tk()
        self.root.title(self.NAME + ' v' + self.VERSION)
        try:
            self.root.iconbitmap('icon.ico')
        except:
            pass
        self.root.geometry('800x600')
        self.root.state('zoomed')

        pygame.mixer.pre_init()
        pygame.mixer.init()
        pygame.init()

        self.loading = True

        Sceleton.__init__(self, self.root)
        self.root.mainloop()
