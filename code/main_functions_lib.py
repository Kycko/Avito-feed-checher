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
def join_multiple_lines(list):
    result = []
    NEXTLINE = False

    for line in list:
        if NEXTLINE:
            if line.count('"') % 2:
                NEXTLINE = False
                if line[:-1] == '"' or line == '"':
                    line = line[:-1]
            result[-1] += line
        elif line.count('"') % 2:
            NEXTLINE = True
            result.append(line[1:])
        else:
            result.append(line)

    for i in range(len(result)):
        result[i] = result[i].replace('""','"')                  # кавычки удваиваются при переносе текста

    return result
def copy_to_clipboard(data):
    result = ''
    for line in data:
        result += line

    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardText(result)
    win32clipboard.CloseClipboard()

# Some specific functions
def plural_word_endings(num, dict):             # num: real number, dict: what dictionary ('words') to use
    words = (('строка', 'строки', 'строк'),
             ('совпадение', 'совпадения', 'совпадений'))

    if all((num % 10 == 1, num % 100 != 11)):
        return words[dict][0]
    elif all((2 <= num % 10 <= 4,
              any((num % 100 < 10, num % 100 >= 20)))):
        return words[dict][1]
    return words[dict][2]
def del_start_end_quotes(string):
    if string[0] == '"':
        string = string[1:]
    if string[-1] == '"':
        string = string[:-1]
    return string
def del_enters_in_list(list):
    for i in range(len(list)):
        if list[i][-1] == '\n':
            list[i] = list[i][:-1]
    return list

# File checking
def prepare_ID_list(file):
    TEMP = read_file(file)
    TEMP = del_enters_in_list(TEMP)
    TEMP = join_multiple_lines(TEMP)
    ID_list = {}

    for line in TEMP:
        # print(line)                                       # for DEBUG
        if line != '\n':
            line = line.lower()                                 # уменьшаем все буквы
            index = line.rfind(",")
            temp_key = line[:index].replace('""','"')           # кавычки удваиваются при экспорте в .csv
            temp_key = del_start_end_quotes(temp_key)
            if line[-1] == "\n":
                line = line[:-1]

            temp_value = line[index+1:]
            temp_value = del_start_end_quotes(temp_value)
            ID_list[temp_key] = temp_value
    # print(ID_list)                              # for DEBUG
    return ID_list
def prepare_FEED_original(list):
    list = join_multiple_lines(list)
    final_list = []
    NEXTLINE = False

    for line in list:
        # print(line)                           # for DEBUG
        line = line.lower()                     # уменьшаем все буквы
        line = line.replace('""','"')   # кавычки удваиваются при копировании
        # print('"' + line + '"')               # for DEBUG
        if line:
            if NEXTLINE:
                if line[-1] == '"':
                    line = line[:-1]
                    NEXTLINE = False
                final_list[-1] += line
            elif line[0] == '"':
                if line[-1] == '"' and len(line) > 1:
                    final_list.append(line[1:-1])
                else:
                    if line.count('"') % 2:
                        NEXTLINE = True
                        final_list.append(line[1:])
                    else:
                        final_list.append(line)
            else:
                final_list.append(line)
        elif not NEXTLINE:
            final_list.append(line)
    # print(final_list)                           # for DEBUG
    return final_list
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
