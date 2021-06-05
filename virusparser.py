import re
import pyperclip


def input():
    # open text file in read mode
    text_file = open("test.txt", "r")

    # read whole file to a string
    data = text_file.read()

    # close file
    text_file.close()
    return data


def virusparser(data: str):
    # replace text
    data = re.sub("^[^/*]*$", "", data, flags=re.MULTILINE)
    data = re.sub("^\n", "", data, flags=re.MULTILINE)
    try:
        pyperclip.copy(data)
        data = data.split("\n")
    except Exception as e:
        data = f"{type(e).__name__} at line {e.__traceback__.tb_lineno} of {__file__}: {e}"
    return data


if __name__ == '__main__':
    print(virusparser(input()))
