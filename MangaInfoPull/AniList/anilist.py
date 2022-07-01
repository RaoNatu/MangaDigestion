from MangaInfoPull.AniList.anilistapi import anilistapi as ani
from time import sleep
from sys import platform
import os

def clear_screen():
    if platform == "linux" or platform == "linux2":
        return "clear"
    else:
        return "cls"

def start_apilist():
    ani_obj = ani()
    mangatitlelinks = []
    os.system(clear_screen())
    manganame = str(input("Search Manga: "))
    mangatitlelinks = ani.search_manga(manganame)
    count = 0

    os.system(clear_screen())
    print("Search Results:")
    for i in mangatitlelinks[0]:
        print(f"{count + 1}. {i}")
        count += 1

    choice = str(input(": "))

    mangainfo = ani.get_manga_info(mangatitlelinks[1][int(choice) - 1])
    os.system(clear_screen())
    ani_obj.show_info(mangainfo)
    sleep(6)