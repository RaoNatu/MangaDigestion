from MangaInfoPull.MyAnimeList.myanimelistapi import myanimelistapi as myani
import os
from sys import platform
from time import sleep

def clear_screen():
    if platform == "linux" or platform == "linux2":
        return "clear"
    else:
        return "cls"

def start_myanimelist():
    os.system(clear_screen())
    titlelinks = []

    manganame = str(input("Search Manga: "))
    titlelinks = myani.search_manga(manganame)
    count = 0

    os.system(clear_screen())

    print("Search Results: ")
    for i in titlelinks[0]:
        print(f"{count + 1}. {titlelinks[0][count]}")
        count += 1

    choice = str(input(": "))

    infols = myani.get_manga_info(titlelinks[1][int(choice) - 1])
    os.system(clear_screen())
    myani.show_info(infols)
    sleep(6)
