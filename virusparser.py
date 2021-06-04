import re
import pyperclip

def input():
    # open text file in read mode
    text_file = open("test.txt", "r")

    # read whole file to a string
    data = text_file.read()

    # close file
    text_file.close()

    # replace text
    data = re.sub("^[^/*]*$", "", data, flags=re.MULTILINE)
    data = re.sub("^\n", "", data, flags=re.MULTILINE)
    #print(repr(data));

    print(data)
    return data

if __name__ == '__main__':
    # TODO Code
    data = input()
    pyperclip.copy(data)