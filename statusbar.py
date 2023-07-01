import os
import tkinter as tk


class StatusBar:

    def __init__(self, statusbar: tk.Frame):
        self.statusbar = statusbar
        self._create_statusbar()

    def _create_statusbar(self):
        self.statusbar_frame1 = tk.Frame(master=self.statusbar)
        self.statusbar_frame1.pack(fill=tk.Y, side=tk.LEFT, expand=0)
        self.statusbar_label1 = tk.Label(master=self.statusbar_frame1, width=30,
                                         text="Audio: " + self.audio_lang.get())
        self.statusbar_label1.pack(fill=tk.Y, side=tk.LEFT, expand=1)
        self.statusbar_label2 = tk.Label(master=self.statusbar_frame1, width=30)
        self.statusbar_label2.pack(fill=tk.Y, side=tk.LEFT, expand=1)
        # self.statusbar_label3 = tk.Label(master=self.statusbar_frame1, width=15,
        #                                  text="Nodes DHT: 0")
        # self.statusbar_label3.pack(fill=tk.Y, side=tk.LEFT, expand=1)
        # self.statusbar_label4 = tk.Label(master=self.statusbar_frame1, width=30,
        #                                  text="D: 0 Bytes/sec")
        # self.statusbar_label4.pack(fill=tk.Y, side=tk.LEFT, expand=1)
        # self.statusbar_label5 = tk.Label(master=self.statusbar_frame1, width=30,
        #                                  text="U: 0 Bytes/sec")
        # self.statusbar_label5.pack(fill=tk.Y, side=tk.LEFT, expand=1)
        self.statusbar_label6 = tk.Label(master=self.statusbar_frame1, width=30, fg="blue", cursor="hand2",
                                         text="Telegram: @syncbooker_chat")
        self.statusbar_label6.pack(fill=tk.BOTH, side=tk.RIGHT, expand=1)
        self.statusbar_label6.bind("<1>", func=lambda _: os.startfile("https://t.me/syncbooker_chat"))
