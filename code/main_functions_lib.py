import pywintypes
import win32clipboard

# File reading/writing
def read_file(filename):
    file = open(filename, 'r', encoding='utf-8')
    data = file.readlines()
    file.close()
    return data
def write_to_the_file(data, filename):
    file = open(filename, 'w', encoding='utf-8')
    file.writelines(data)
    file.close()
def copy_to_clipboard(data):
    result = ''
    for line in data:
        result += line

    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardText(result)
    win32clipboard.CloseClipboard()

# Preparing lists from files
def del_enters_in_list(list):                           # ТОЛЬКО удаляем переносы строки в конце каждого элемента списка
    for i in range(len(list)):
        if list[i][-1] == '\n':
            list[i] = list[i][:-1]
    return list
def join_multiple_lines(list, enters_warning=False):    # ТОЛЬКО соединяем несколько строк из одной ячейки в одну строку
    result = []
    NEXTLINE = False
    idlist_enters = 0                                   # Для оповещения о наличии переноса в списке Type ID

    for line in list:
        idlist_enters += 1
        if NEXTLINE:
            result[-1] += line
            if line and line[-1] == '"' and line.count('"') % 2:
                NEXTLINE = False
        else:
            result.append(line)
            if line and line[0] == '"' and line.count('"') % 2:
                NEXTLINE = True
                if enters_warning:
                    print('!!!Несколько строк в одной ячейке строки [' + str(idlist_enters) + ']!!!')
                    print('--------------------------------------------------')
                    print()

    return result
def rm_both_starting_and_ending_quotes(list):       # Удаляем кавычки с обеих сторон, ТОЛЬКО если они есть с обеих сторон
    for i in range(len(list)):
        if len(list[i]) > 1 and list[i][0] == '"' and list[i][-1] == '"':
            list[i] = list[i][1:-1]
    return list
def rm_doubled_quotes(list):                        # ТОЛЬКО меняем двойные кавычки на одинарные (двоятся при копировании)
    for i in range(len(list)):
        list[i] = list[i].replace('""','"')
    return list
def rm_ending_space(list):                          # ТОЛЬКО удаляем лишние пробелы в конце строк
    for i in range(len(list)):
        while list[i] and list[i][-1] == ' ':
            list[i] = list[i][:-1]
    return list
def make_list_lower(list):                          # ТОЛЬКО превращаем ВСЕ буквы в строчные
    for i in range(len(list)):
        list[i] = list[i].lower()
    return list

# Some specific functions
def plural_word_endings(num, dict):                 # num: real number, dict: what dictionary ('words') to use
    words = (('строка', 'строки', 'строк'),
             ('совпадение', 'совпадения', 'совпадений'))

    if all((num % 10 == 1, num % 100 != 11)):
        return words[dict][0]
    elif all((2 <= num % 10 <= 4,
              any((num % 100 < 10, num % 100 >= 20)))):
        return words[dict][1]
    return words[dict][2]

# File checking
def prepare_ID_list(file):
    list = read_file(file)
    list = del_enters_in_list(list)
    list = join_multiple_lines(list, True)
    # print(list)                       # for DEBUG

    multilist = [[], []]                # [KEYS, VALUES]
    for line in list:                   # Делим на отдельные списки ключи и значения, чтобы убрать из них всё лишнее и затем соединить в словарь
        if line:
            index = line.rfind(",")
            multilist[0].append(line[:index])
            multilist[1].append(line[index+1:])
    for i in range(2):
        multilist[i] = rm_both_starting_and_ending_quotes(multilist[i])
        multilist[i] = rm_doubled_quotes(multilist[i])
        multilist[i] = make_list_lower(multilist[i])
        multilist[i] = rm_ending_space(multilist[i])
        # print(multilist[i])                           # for DEBUG

    ID_list = {}
    doubles_counter = 0
    for i in range(len(multilist[0])):
        if multilist[0][i] in ID_list:
            print('Дубль записи в списке Type ID: ' + multilist[0][i])
            doubles_counter += 1
        ID_list[multilist[0][i]] = multilist[1][i]

    # print(ID_list)                                    # for DEBUG
    if doubles_counter:
        print('--------------------------------------------------')
        print('Всего дублей: ' + str(doubles_counter))
        print('--------------------------------------------------')
        print()
    return ID_list
def prepare_FEED_original(list):
    list = join_multiple_lines(list)
    list = rm_both_starting_and_ending_quotes(list)
    list = rm_doubled_quotes(list)
    list = make_list_lower(list)

    # print(list)       # for DEBUG
    return list
def MAIN_CYCLE(FEED_original, ID_list):
    FINAL_ID_list = []
    FOUND_IDs_counter = 0
    len_feed = len(FEED_original)

    print('                                                  ', end='\r')
    for index in range(len_feed):
        percent = str(int(100*(index+1)/len_feed))
        print('Обработано: ' + percent + '%', end='\r')

        FOUND_ID = {}
        for key in ID_list.keys():
            STR_FOUND = FEED_original[index].find(key)
            if STR_FOUND > -1:                          # Если -1, значит, ничего не найдено.
                FOUND_ID[key] = ID_list[key]
        if len(FOUND_ID):
            maxlenth = 0
            maxkey = ""
            for i in FOUND_ID.keys():
                if len(i) > maxlenth:
                    maxlenth = len(i)
                    maxkey = i
            FINAL_ID_list.append(FOUND_ID[maxkey] + "\n")
            FOUND_IDs_counter += 1
        else:
            FINAL_ID_list.append("\n")
    return FOUND_IDs_counter, FINAL_ID_list
