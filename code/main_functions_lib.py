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

# Some specific functions
def plural_word_endings(num):
    words = ['строка', 'строки', 'строк']

    if all((num % 10 == 1, num % 100 != 11)):
        return words[0]
    elif all((2 <= num % 10 <= 4,
              any((num % 100 < 10, num % 100 >= 20)))):
        return words[1]
    return words[2]

# File checking
def prepare_ID_list(file):
    TEMP = read_file(file)
    ID_list = {}

    for line in TEMP:
        # print(line)                                       # for DEBUG
        if line != '\n':
            line = line.lower()                                 # уменьшаем все буквы
            index = line.rfind(",")
            temp_key = line[:index].replace('""','"')           # кавычки удваиваются при экспорте в .csv
            if temp_key[0] == '"':
                temp_key = temp_key[1:]
            if temp_key[-1] == '"':
                temp_key = temp_key[:-1]
            if line[-1] == "\n":
                line = line[:-1]

            temp_value = line[index+1:]
            ID_list[temp_key] = temp_value
    return ID_list
def prepare_FEED_original(list):
    final_list = []
    NEXTLINE = False

    for line in list:
        # print(line)                           # for DEBUG
        line = line.lower()                     # уменьшаем все буквы
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
        else:
            final_list.append(line)
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
