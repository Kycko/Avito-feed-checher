from os import path as OSpath
# import win32clipboard
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
print("Checking args...")

if len(sys.argv) == 1:
    FUNC_exit_with_error("PLEASE ADD A FILENAME")
for i in [1, 2]:
    if not OSpath.isfile(sys.argv[i]):
        FUNC_exit_with_error("NOT FOUND: "+sys.argv[i])

print("Preparing FEED file.............", end="")
TEMP = FUNC_read_file(sys.argv[1])
FEED_original = []
NEXTLINE = False

for line in TEMP:
    # print(line)                       # for DEBUG
    line = line[:-1].lower()            # отрезаем перенос строки и уменьшаем все буквы
    if NEXTLINE:
        if line[-1] == '"':
            line = line[:-1]
            NEXTLINE = False
        FEED_original[-1] += line
    elif line[0] == '"':
        if line[-1] == '"':
            FEED_original.append(line[1:-1])
        else:
            if line.count('"') % 2:
                NEXTLINE = True
                FEED_original.append(line[1:])
            else:
                FEED_original.append(line)
    else:
        FEED_original.append(line)
print(str(len(FEED_original)) + " items")


print("Preparing ID list...............", end="")
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

# print(FEED_original[1000])                             # for DEBUG
input("Press ENTER to continue...")


# MAIN CYCLE
FINAL_ID_list = []
FOUND_IDs_counter = 0
for index in range(len(FEED_original)):
    print("Searching Type ID for item №...." + str(index+1), end="\r")
    FOUND_ID = {}
    for key in ID_list.keys():
        STR_FOUND = FEED_original[index].find(key)
        if STR_FOUND > -1:                                                            # Если -1, значит, ничего не найдено.
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


# finalizing
final_filename   = "KEYS FOR " + sys.argv[1][2:]
final_percentage = 100*FOUND_IDs_counter/len(FEED_original)

# win32clipboard.OpenClipboard()
# win32clipboard.EmptyClipboard()
# win32clipboard.SetClipboardText(FINAL_ID_list)
# win32clipboard.CloseClipboard()

print()                                                                             # перевод на новую строку в конце программы
print("Writing to the file...")
print()
FUNC_write_to_the_file(FINAL_ID_list, final_filename)
print("-------------------------------------------")
print("DONE!")
print("Found IDs:......................" + str(FOUND_IDs_counter), end=" ")
print("(" + str(final_percentage)[:4] + "%)")
print()
print("Your IDs was written to this file:")
print("   " + final_filename)
print("-------------------------------------------")
