import re


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
    return data


if __name__ == '__main__':
    print(virusparser(input()))
