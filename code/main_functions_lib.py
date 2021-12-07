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