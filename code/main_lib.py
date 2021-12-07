import tkinter as tk

class APP(tk.Tk):
    def __init__(self):
        super().__init__()
        self.win_width  = 670                               # main window size
        self.win_height = 685                               # main window size
        self.win_title  = 'Avito feed checker (запчасти)'   # main window title

        self.files = []

        self.geometry(str(self.win_width) + "x" + str(self.win_height))
        self.title(self.win_title)
        self.resizable(0,0)                                 # makes the app window unresizable

        self.buttons = {}                                   # all the buttons of the app
        for i in range(2):
            self.buttons['btn'+str(i)] = tk.Button(self, padx=10, pady=3, height=1, width=33)
            self.buttons['btn'+str(i)].grid(column=0, row=i, columnspan=2, padx=7, pady=15-(i*15), sticky=tk.E)
        self.buttons['btn0']['text']    = 'Выбрать список названий с Type ID'
        self.buttons['btn1']['text']    = 'Выбрать список OEM-номеров с Type ID'
        self.buttons['btn0']['command'] = self.btn0_clicked
        self.buttons['btn1']['command'] = self.btn1_clicked

        self.labels = {}                                    # all the labels of the app
        for i in range(2):
            self.labels['lbl'+str(i)] = {}
            self.labels['lbl'+str(i)]['obj'] = tk.Label(self, padx=12, pady=5, width=47, anchor='w', relief=tk.GROOVE)
            self.labels['lbl'+str(i)]['obj'].grid(column=2, row=i, columnspan=2, padx=15, sticky=tk.W)
    def btn0_clicked(self):
        print('btn0_clicked')
    def btn1_clicked(self):
        print('btn1_clicked')
