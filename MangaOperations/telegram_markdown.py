import os
from natsort import natsorted
from sys import platform


def tele_markdown(path):
    manga_name = os.listdir(path)
    if platform == "linux" or platform == "linux2":
        path = path + "/"
    else:
        path = path + "\\"

    str = """❗ **On going Manga Updates:**"""
    manga_name = sorted(manga_name)
    for i in manga_name:
        chapter_num = os.listdir(path + i)
        chapter_num = natsorted(chapter_num)
        temp = []
        for j in chapter_num:
            temp.append("CH " + j.split(" ")[1] + ", ")
        str += "\n⛩ " + i[:-4] + " "
        for t in temp:
            str += t
    temp_str_split = str.split("\n")
    str = """❗ **On going Manga Updates:**"""
    for i in temp_str_split[1:]:
        str += "\n" + i[:-2]
    print()
    print(str)
