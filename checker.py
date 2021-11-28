from os import path as OSpath
import sys

# functions
def FUNC_exit_with_error(error_code):
    print()
    print("------------------------------")
    print(error_code)
    print("Exit...")
    sys.exit()
def FUNC_read_file(filename):
    file = open(filename, 'r', encoding='utf-8')
    data = file.readlines()
    file.close()
    return data
def FUNC_write_to_the_file(data, filename):
    file = open(filename, 'w', encoding='utf-8')
    file.writelines(data)
    file.close()

# MAIN PROGRAM
print("------------------------------")
print("Checking args...")

if len(sys.argv) == 1:
    FUNC_exit_with_error("PLEASE ADD A FILENAME")
for i in [1, 2]:
    if not OSpath.isfile(sys.argv[i]):
        FUNC_exit_with_error("NOT FOUND: "+sys.argv[i])

print("Preparing FEED file....", end="")
TEMP = FUNC_read_file(sys.argv[1])
FEED_original = []
NEXTLINE = False

for line in TEMP:
    line = line[:-1].lower()            # отрезаем перенос строки и уменьшаем все буквы
    if NEXTLINE:
        if line[-1] == '"':
            line = line[:-1]
            NEXTLINE = False
        FEED_original[-1] += line
    elif line[0] == '"':
        if line[-1] == '"':
            line = line[:-1]
        else:
            NEXTLINE = True
        FEED_original.append(line[1:])
    else:
        FEED_original.append(line)
print(str(len(FEED_original)) + " items")


print("Preparing ID list......", end="")
TEMP = FUNC_read_file(sys.argv[2])
ID_list = {}

for line in TEMP:
    line = line.lower()                                 # уменьшаем все буквы
    index = line.rfind(",")
    temp_key = line[:index].replace('""','"')           # кавычки удваиваются при экспорте в .csv
    if temp_key[0] == '"':
        temp_key = temp_key[1:]
    if temp_key[-1] == '"':
        temp_key = temp_key[:-1]

    temp_value = line[index+1:-1]
    ID_list[temp_key] = temp_value
print(str(len(ID_list)) + " items")



# for key in ID_list.keys():
    # print(ID_list[key] + " || " + key)

# for index in range(len(FEED_original)):
#     # for key in ID_list.keys():
#     #     STR_FOUND = FUNC_find_substring(key, FEED_original[index])
#     #     if STR_FOUND:
#     #         print(FEED_original[index][:-1] + " || " + key + " || " + ID_list[key])
#
#
#     string = FEED_original[index]
#     STR_FOUND = string.find(substring)("Гайка", "Гайка")
#     if STR_FOUND > -1:                                                                      # Если -1, значит, ничего не найдено.
#         print(FEED_original[index][:-1] + " || " + "гайка" + " || " + ID_list["Гайка"])


# temp = FUNC_find_substring_return_before(".txt", sys.argv[1])
# NEW_filename = temp+" formatted.csv"
#
# # making the first few mandatory lines
# print("Making the first few mandatory lines...")
#
# for string in DATA_original:
#     tempTEXT = FUNC_find_substring_return_after("string m_Name = ", string, 1)
#     if tempTEXT:
#         DATA_new = ['Key,' + tempTEXT[1:-1] + ',NOTES,' + NEW_filename + ',\n',
#                     ',,,,,,,,,,,,,,,,,,,\n',
#                     'UseCyrillicFont,No,"Пометка для переводчиков: поставьте на позиции (между разделителями) вашего языка «Yes», если используете кириллицу",Yes,\n',
#                     ',,,,,,,,,,,,,,,,,,,\n']
#         break
#
# # check total amount of KEYS
# temp_counter = False
# for string in DATA_original:
#     tempTEXT = FUNC_find_substring_return_after("int size = ", string, 1)
#     if tempTEXT:
#         if temp_counter:
#             print("KEYS total....................."+tempTEXT)
#             break
#         else:
#             temp_counter = True
#
# # making KEYS + ingame strings
# print("Making KEYS + ingame strings...", end="")
#
# string_counter = 0
# key_is_opened = False
#
# for string in DATA_original:
#     if key_is_opened:
#         if string[0] == '\t':
#             DATA_new[-1] += ',,,\n'
#             key_is_opened = False
#         else:
#             DATA_new[-1] += '\n'
#             DATA_new.append(string[:-1])
#     else:
#         tempTEXT = FUNC_find_substring_return_after("string m_Key = ", string, 1)
#         if tempTEXT:
#             string_counter += 1
#             print("\rMaking KEYS + ingame strings..."+str(string_counter), end="")
#             DATA_new.append(tempTEXT[1:-1]+',')
#         elif string_counter:
#             tempTEXT = FUNC_find_substring_return_after("string data = ", string, 1)
#             if tempTEXT:
#                 DATA_new[-1] += tempTEXT
#                 key_is_opened = True
#
# # finalizing
# print()
# print("Writing to the file...")
# FUNC_write_to_the_file(DATA_new, NEW_filename)
# print()
# print("------------------------------")
# print("DONE! Check this file:")
# print(" "+NEW_filename)
# print("------------------------------")
