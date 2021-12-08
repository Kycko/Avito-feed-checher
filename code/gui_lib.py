import global_vars as Globals
import main_functions_lib as FUNC
import tkinter as tk
from os import path as OSpath
from tkinter import filedialog
from tkinter import scrolledtext
import tkinter.font as TKfont

class APP(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry(str(Globals.app_width) + "x" + str(Globals.app_height))
        self.title(Globals.app_title)
        self.resizable(0,0)                                                 # makes the app window unresizable

        # Buttons for files choosing
        self.buttons = {'btn0' : tk.Button(self,
                                           text='Выбрать список Type ID',
                                           command=self.btn0_clicked,
                                           padx=10,
                                           pady=3,
                                           height=1,
                                           width=33)}
        self.buttons['btn0'].grid(column=0, row=0, columnspan=2, padx=5, pady=10, sticky=tk.E)

        # Labels for files choosing
        self.labels = {'lbl0' : tk.Label(self,
                                         padx=12,
                                         pady=5,
                                         width=47,
                                         text='Не выбрано',
                                         foreground=Globals.COLORS['red'],
                                         anchor='w',
                                         relief=tk.GROOVE)}
        self.labels['lbl0'].grid(column=2, row=0, columnspan=2, padx=15, sticky=tk.W)

        # Hint text (label) for client's feed
        text = ''
        for i in range(129):
            text += '-'
        text += """
↓ Вставьте в поле ниже список наименований из фида клиента. Желательно удалить все лишние строки снизу. ↓"""
        self.labels['feed_hint'] = tk.Label(self, text=text, justify=tk.LEFT, anchor='w')
        self.labels['feed_hint'].grid(column=0, row=1, columnspan=4, padx=5, sticky=tk.W)

        # Text field for client's feed
        self.clients_feed_list = scrolledtext.ScrolledText(self, width=80, height=27)
        self.clients_feed_list.grid(column=0, row=2, columnspan=4, padx=5, pady=7)

        # Start main processing button
        self.buttons['MAIN_START'] = tk.Button(self,
                                               font=TKfont.Font(family='Arial', size=13),
                                               command=self.MAIN_START_clicked,
                                               padx=10,
                                               pady=3,
                                               height=5)
        self.buttons['MAIN_START'].grid(column=3, row=3, padx=10, pady=5, sticky=tk.E)

        # Button & label for client's feed strings counter
        self.buttons['count_feed'] = tk.Button(self,
                                               text="Посчитать строки",
                                               command=self.count_feed_clicked,
                                               padx=10,
                                               pady=3,
                                               height=2)
        self.buttons['count_feed'].grid(column=0, row=3, padx=10, pady=10, sticky=tk.N)

        self.labels['feed_counter'] = tk.Label(self,
                                               padx=12,
                                               pady=12,
                                               width=25,
                                               relief=tk.GROOVE)
        self.labels['feed_counter'].grid(column=1, row=3, columnspan=2, padx=10, pady=10, sticky=tk.NW)

        # Init settings
        init_checkbox = self.init_settings()

        # 'Copy to clipboard' checkbox
        self.checkboxes = {}
        self.checkboxes['clipboard'] = {'var' : tk.BooleanVar(value=init_checkbox)}
        self.checkboxes['clipboard']['obj'] = tk.Checkbutton(self,
                                                             text='Скопировать результат в буфер обмена',
                                                             variable=self.checkboxes['clipboard']['var'],
                                                             onvalue=True,
                                                             offvalue=False)
        self.checkboxes['clipboard']['obj'].grid(column=1, row=4, columnspan=3, padx=10, sticky=tk.E)

        self.count_feed_clicked()
        self.clients_feed_list.focus_set()
    def save_settings(self):
        clipboard_setting = str(int(self.checkboxes['clipboard']['var'].get()))
        data = [clipboard_setting + '\n',
                self.file+'\n']
        FUNC.write_to_the_file(data, 'settings')
    def init_settings(self):
        self.file          = ''                                         # only the path to the file
        self.IDlist        = {'obj' : '', 'count' : 0, 'ready' : False} # ID list as a reference to check
        self.FEED_original = {'obj' : '', 'count' : 0, 'ready' : False} # client's feed names list

        if OSpath.isfile('settings'):
            data = FUNC.read_file('settings')
            file_path = data[1][:-1]      # without '\n'
            if OSpath.isfile(file_path):
                self.file = file_path
                self.file_choose_clicked()
            return bool(int(data[0][:-1]))
        return True
    def btn0_clicked(self):
        self.file = filedialog.askopenfilename(initialdir= OSpath.dirname(__file__))
        self.file_choose_clicked()
    def file_choose_clicked(self):
        if self.file:
            text = OSpath.basename(self.file)[:40]
            if self.file[-4:] in (".csv", ".txt"):
                color = Globals.COLORS['green']
                self.IDlist['obj']   = FUNC.prepare_ID_list(self.file)
                self.IDlist['count'] = len(self.IDlist['obj'])
                self.IDlist['ready'] = True                     # it means "ready to start main processing"
                text = ''.join(['[',
                                str(self.IDlist['count']),
                                ' ',
                                FUNC.plural_word_endings(self.IDlist['count'], 0),
                                '] ',
                                text])
            else:
                color = Globals.COLORS['red']
                self.IDlist['ready'] = False
            self.labels['lbl0'].config(foreground=color, text=text)
        self.check_main_start_state()
    def count_feed_clicked(self):
        TEMP = self.clients_feed_list.get("1.0", tk.END)
        TEMP = list(TEMP.split("\n"))
        self.FEED_original['obj'] = FUNC.prepare_FEED_original(TEMP)

        counter = 0
        for i in range(len(self.FEED_original['obj'])):
            if self.FEED_original['obj'][i]:
                counter += 1
        self.FEED_original['count'] = counter

        self.FEED_original['ready'] = bool(counter)

        text = str(self.FEED_original['count']) + ' ' + FUNC.plural_word_endings(self.FEED_original['count'], 0)
        color = ('red', 'green')[self.FEED_original['ready']]
        self.labels['feed_counter'].config(text       = text,
                                           foreground = Globals.COLORS[color])
        self.check_main_start_state()
    def check_main_start_state(self):
        if self.ready_for_MAIN_START_condition():
            self.buttons['MAIN_START']["state"] = "normal"
            self.buttons['MAIN_START']["text"] = "ЗАПУСТИТЬ\n»»»"
        else:
            self.buttons['MAIN_START']["state"] = "disabled"
            self.buttons['MAIN_START']["text"] = "ЗАПУСТИТЬ\nxxx"
    def ready_for_MAIN_START_condition(self):
        return self.FEED_original['ready'] and self.IDlist['ready']
    def MAIN_START_clicked(self):
        self.count_feed_clicked()
        if self.ready_for_MAIN_START_condition():
            self.save_settings()
            count, RESULT = FUNC.MAIN_CYCLE(self.FEED_original['obj'], self.IDlist['obj'])
            FUNC.write_to_the_file(RESULT, Globals.FILES['result'])
            text = ''
            if self.checkboxes['clipboard']['var'].get():
                FUNC.copy_to_clipboard(RESULT)
                text = 'уже скопирован в буфер обмена\nи '

            percent = 100*count/self.FEED_original['count']
            text = ''.join(['Найдено ',
                            str(count),
                            ' ',
                            FUNC.plural_word_endings(count, 1),
                            ' ({0:.1f}%).'.format(percent),
                            '\n\nСписок Type ID ',
                            text,
                            'сохранён в файле\n"',
                            Globals.FILES['result'],
                            '".'])

            tk.messagebox.showinfo('Готово!', text)
            self.destroy()
