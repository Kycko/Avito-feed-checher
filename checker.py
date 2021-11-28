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
    file = open(filename, 'r', encoding='utf-8-sig')
    data = file.readlines()
    file.close()
    return data
def FUNC_write_to_the_file(data, filename):
    file = open(filename, 'w', encoding='utf-8')
    file.writelines(data)
    file.close()


def FUNC_find_substring(substring, string):
    index = string.find(substring)
    if index == -1:
        return 0
    else:
        return index
def FUNC_find_substring_return_after(substring, string, remove_newline):                # string, string, int(0/1)
    index = FUNC_find_substring(substring, string)
    if index:
        cut_from = index+len(substring)
        return string[cut_from:len(string)-1*remove_newline]
    else:
        return ""
def FUNC_find_substring_return_before(substring, string):
    index = FUNC_find_substring(substring, string)
    if index:
        return string[:index]
    else:
        return string

# MAIN PROGRAM
print("------------------------------")
print("Prepare...")

if len(sys.argv) == 1:
    FUNC_exit_with_error("PLEASE ADD A FILENAME")
for i in [1, 2]:
    if not OSpath.isfile(sys.argv[i]):
        FUNC_exit_with_error("NOT FOUND: "+sys.argv[i])

print("Reading files...")
FEED_original = FUNC_read_file(sys.argv[1])
TEMP = FUNC_read_file(sys.argv[2])

print("Making ID list...")
ID_list = {}
for string in TEMP:
    index = string.rfind(",")

    temp_key = string[:index].replace('""','"')
    if temp_key[0] == '"':
        temp_key = temp_key[1:]
    if temp_key[len(temp_key)-1] == '"':
        temp_key = temp_key[:len(temp_key)-1]

    temp_value = string[index+1:len(string)-1]
    ID_list[temp_key] = temp_value


for key in ID_list.keys():
    print(ID_list[key] + " : " + key)

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
