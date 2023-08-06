import os


def readlines(file_name):
    f = open(os.path.abspath(file_name))
    lines = f.readlines()
    f.close()
    return lines


def writelines(lines, file_name):
    f = open(file_name, 'w')
    f.writelines(lines)
    f.close()
