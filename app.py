import tkinter as tk
from sceleton import Sceleton
import pygame


class App(Sceleton):
    NAME = 'SyncBooker'
    VERSION = '1.3'

    def __init__(self):

        self.root = tk.Tk()
        self.root.title(self.NAME + ' v' + self.VERSION)
        self.root.iconbitmap('icon.ico')
        self.root.geometry('800x600')
        self.root.state('zoomed')

        pygame.mixer.pre_init()
        pygame.mixer.init()
        pygame.init()

        Sceleton.__init__(self, self.root)
        self.root.mainloop()
