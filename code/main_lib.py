from os import path as OSpath
from sys import exit as SYSexit
from tkinter import *
from tkinter import filedialog
from tkinter import scrolledtext

# Basic functions
def FUNC_exit_with_error(error_code):
    print()
    print("------------------------------")
    print(error_code)
    print("Exit...")
    SYSexit()
def FUNC_read_file(filename):
    file = open(filename, 'r', encoding='utf-8')
    data = file.readlines()
    file.close()
    return data
def FUNC_write_to_the_file(data, filename):
    file = open(filename, 'w', encoding='utf-8')
    file.writelines(data)
    file.close()

# Some checking functions
def check_file_extention(file):
    return file[-4:] in (".csv", ".txt")

# Button actions
def button_1_clicked():
    global file_1
    file_1 = filedialog.askopenfilename(initialdir= OSpath.dirname(__file__))
    file_choose_clicked(lbl_1, file_1)
def button_2_clicked():
    global file_2
    file_2 = filedialog.askopenfilename(initialdir= OSpath.dirname(__file__))
    file_choose_clicked(lbl_2, file_2)
def file_choose_clicked(lbl, file):
    lbl.config(text=OSpath.basename(file)[:40])
    good_ext = check_file_extention(file)
    if good_ext:
        lbl.config(foreground=COLOUR_green)
    else:
        lbl.config(foreground=COLOUR_red)

# Making GUI
def FUNC_GUI_init():
    window = Tk()
    window.geometry(str(app_width) + "x" + str(app_height))
    window.title(window_title)
    window.resizable(0,0)                                       # makes the app window unresizable

    # First button group
    global lbl_1
    button_1 = Button(window, text="Выбрать список названий с Type ID", command=button_1_clicked, padx=10, pady=3, height = 1, width = 33)
    button_1.grid(column=0, row=0, pady=15, sticky=E)
    lbl_1 = Label(window, text=lbl_1_2_text, foreground=COLOUR_red, padx=22, pady=10, width=50, anchor='w')
    lbl_1.grid(column=1, row=0, sticky=W)

    # Second button group
    global lbl_2
    button_2 = Button(window, text="Выбрать список OEM-номеров с Type ID", command=button_2_clicked, padx=10, pady=3, height = 1, width = 33)
    button_2.grid(column=0, row=1, sticky=E)
    lbl_2 = Label(window, text=lbl_1_2_text, foreground=COLOUR_red, padx=22, pady=10, width=50, anchor='w')
    lbl_2.grid(column=1, row=1, sticky=W)

    # Text field for client's feed
    clients_feed_list = scrolledtext.ScrolledText(window, width=80, height=30)
    clients_feed_list.grid(column=0, row=2, columnspan=2, padx=5, pady=20)
    return window

# Global vars
app_width = 700
app_height = 700
window_title = "Avito feed checker (запчасти)"

# Colours
COLOUR_red = "#D73B41"
COLOUR_green ="#14963A"

# Label vars
lbl_1_2_text = "Не выбрано"
