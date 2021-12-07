import tkinter as tk

class APP(tk.Tk):
    def __init__(self):
        super().__init__()
        self.win_width  = 670                               # main window size
        self.win_height = 685                               # main window size
        self.win_title  = "Avito feed checker (запчасти)"   # main window title

        self.geometry(str(self.win_width) + "x" + str(self.win_height))
        self.title(self.win_title)
        self.resizable(0,0)                                 # makes the app window unresizable
