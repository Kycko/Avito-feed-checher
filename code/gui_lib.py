import global_vars as Globals
import main_functions_lib as FUNC
import tkinter as tk
from os import path as OSpath
from tkinter import filedialog

class APP(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry(str(Globals.app_width) + "x" + str(Globals.app_height))
        self.title(Globals.app_title)
        self.resizable(0,0)                                             # makes the app window unresizable

        self.files   = ['', '']                                         # only the path to each file
        self.IDlists = [{}, {}]                                         # ID lists as a reference to check

        self.buttons = {}                                               # all the buttons of the app
        for i in range(2):
            self.buttons['btn'+str(i)] = tk.Button(self, padx=10, pady=3, height=1, width=33)
            self.buttons['btn'+str(i)].grid(column=0, row=i, columnspan=2, padx=7, pady=15-(i*15), sticky=tk.E)
        self.buttons['btn0']['text']    = 'Выбрать список названий с Type ID'
        self.buttons['btn1']['text']    = 'Выбрать список OEM-номеров с Type ID'
        self.buttons['btn0']['command'] = self.btn0_clicked
        self.buttons['btn1']['command'] = self.btn1_clicked

        self.labels = {}                                                # all the labels of the app
        for i in range(2):
            self.labels['lbl'+str(i)] = {'num'      : i,
                                         'obj'      : tk.Label(self,
                                                               padx=12,
                                                               pady=5,
                                                               width=47,
                                                               text='Не выбрано',
                                                               foreground=Globals.COLORS['red'],
                                                               anchor='w',
                                                               relief=tk.GROOVE)}
            self.labels['lbl'+str(i)]['obj'].grid(column=2, row=i, columnspan=2, padx=15, sticky=tk.W)
    def btn0_clicked(self):
        self.files[0] = filedialog.askopenfilename(initialdir= OSpath.dirname(__file__))
        self.file_choose_clicked(0)
    def btn1_clicked(self):
        self.files[1] = filedialog.askopenfilename(initialdir= OSpath.dirname(__file__))
        self.file_choose_clicked(1)
    def file_choose_clicked(self, num):
        if self.files[num]:
            text = OSpath.basename(self.files[num])[:40]
            if self.files[num][-4:] in (".csv", ".txt"):
                color = Globals.COLORS['green']
                self.IDlists[num]['obj']   = FUNC.prepare_ID_list(self.files[num])
                self.IDlists[num]['count'] = len(self.IDlists[num]['obj'])
                self.IDlists[num]['ready'] = True           # it means "ready to start main processing"
                text = ''.join(['[',
                                str(self.IDlists[num]['count']),
                                ' ',
                                FUNC.plural_word_endings(self.IDlists[num]['count']),
                                '] ',
                                text])
            else:
                color = Globals.COLORS['red']
                self.IDlists[num]['ready'] = False
            self.labels['lbl'+str(num)]['obj'].config(foreground=color, text=text)
        # FUNC_check_main_start_state()                         # to be done later
