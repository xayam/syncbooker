import tkinter as tk
from controller.player import Player


class ToolBar(Player):
    def __init__(self, app):
        self.app = app
        self.app.toolbar = self.app.sceleton_toolbar
        self.pause_len = 0
        self.flag_pause = True
        self.pos_end = 0
        self.start = 0
        self.line_count = 0
        self.sync_i = 0
        self.pos_end_other = 0
        self.sync_other_i = 0
        self._create_toolbar()
        Player.__init__(self, app=self)

    def _create_toolbar(self):
        self.frame_right_navigator = tk.Frame(self.app.toolbar)

        empty1 = tk.Label(master=self.frame_right_navigator, text="", font=("Aerial", 20), width=1)
        empty1.pack(fill=tk.BOTH, side=tk.LEFT, expand=False)

        empty2 = tk.Label(master=self.frame_right_navigator, text="", font=("Aerial", 20), width=14)
        empty2.pack(fill=tk.BOTH, side=tk.LEFT, expand=False)

        empty3 = tk.Label(master=self.frame_right_navigator, text="", font=("Aerial", 20), width=1)
        empty3.pack(fill=tk.BOTH, side=tk.LEFT, expand=False)

        self.backward_button = tk.Button(master=self.frame_right_navigator,
                                         text=u"\u23ee",
                                         font=("Aerial", 20),
                                         command=self.app.backward
                                         )
        self.backward_button.pack(fill=tk.BOTH, side=tk.LEFT, expand=False)
        self.play_button = tk.Button(master=self.frame_right_navigator,
                                     text=u"\u23f5",
                                     font=("Aerial", 20),
                                     command=self.app.play
                                     )
        self.play_button.pack(fill=tk.BOTH, side=tk.LEFT, expand=False)
        self.pause_button = tk.Button(master=self.frame_right_navigator,
                                      text=u"\u23f8",
                                      font=("Aerial", 20),
                                      command=self.app.pause
                                      )
        self.pause_button.pack(fill=tk.BOTH, side=tk.LEFT, expand=False)
        self.stop_button = tk.Button(master=self.frame_right_navigator,
                                     text=u"\u23f9",
                                     font=("Aerial", 20),
                                     command=self.app.stop
                                     )
        self.stop_button.pack(fill=tk.BOTH, side=tk.LEFT, expand=False)
        self.forward_button = tk.Button(master=self.frame_right_navigator,
                                        text=u"\u23ed",
                                        font=("Aerial", 20),
                                        command=self.app.forward
                                        )
        self.forward_button.pack(fill=tk.BOTH, side=tk.LEFT, expand=False)
