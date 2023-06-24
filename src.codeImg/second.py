from tkinter import Tk, Label
from typing import List

from PIL import ImageTk, Image
import string

def generate_combinations(n):
    all = list(string.ascii_lowercase + "0123456789")
    if n == 0:
        return []
    elif n == 1:
        return all
    else:
        combinations = []
        for combination in generate_combinations(n - 1):
            for digit in all:
                combinations.append(combination + digit)
        return combinations


def formatCombin(needFormat):
    count = needFormat.count("*")
    needFormat = needFormat.replace("*", "{}")
    allCombine = generate_combinations(count)
    result = []
    for posiable in allCombine:
        l: list[str] = list(posiable)
        format_format = needFormat.format(*l)
        result.append(format_format)
    return result


if __name__ == '__main__':
    combin = formatCombin("AAAAAAA*A*")
    for str123 in combin:
        print(str123)
