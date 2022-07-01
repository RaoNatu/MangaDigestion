import os
import re
from sys import platform
import requests
import json
import time
from bs4 import BeautifulSoup


def clear_screen():
    if platform == "linux" or platform == "linux2":
        return "clear"
    else:
        return "cls"


def find():
    url = "https://mangakakalot.com/manga_list"
    manga_info = []
    link_info = []
    name_link = {}
    last_page = 1
    current_page = 0
    if os.path.exists("Mangakakalot_manga_list.json"):
        print("File 'Mangakakalot_manga_list' Already Exists")
    else:
        while current_page <= last_page:
            info = []
            r = requests.get(f"{url}?page={current_page}")
            soup = BeautifulSoup(r.text, 'html.parser')
            for i, row in enumerate(soup.find_all('div', class_="list-truyen-item-wrap")):
                info.append(row.text)
                link_info.append(row.a['href'])

            for i in info:
                temp = i.split('\n')
                temp_ls = []
                for j in temp:
                    if j != "":
                        temp_ls.append(j)
                manga_info.append(temp_ls)

            titles = [x[0] for x in manga_info]
            last_page = str(soup.find_all('a', class_="page_blue page_last"))
            last_page = int(re.search(r'\d+', str(last_page)).group(0))
            print(f"{current_page}/{last_page}")
            current_page += 1

            if len(titles) == len(link_info):
                for i in range(len(titles)):
                    name_link[titles[i]] = link_info[i]
            else:
                print("Hmm... Length is not equal!")
                time.sleep(5)
            with open("Mangakakalot_manga_list.json", "w") as f:
                f.write(json.dumps(name_link))
                print("File Updated!")


def search():
    is_on = True
    titles = {}
    searched = {}

    try:
        with open(f"{os.getcwd()}/MangaInfoPull/Mangakakalot/Mangakakalot_manga_list.json", "r") as f:
            manga_link = json.load(f)
    except:
        print("File Doesn't Exist!")

    while is_on:
        searched = {}
        # print(manga_link)
        search_str = str(input("Search Manga: "))

        # Searching Via Regex
        os.system(clear_screen())
        print(f"Searched results for: \"{search_str}\"")

        for i in manga_link:
            try:
                x = re.search(r'^' + f'{search_str}' + r"[\w :\d\-'&,!?.]+$", str(i)).group(0)
                searched[i] = manga_link[i]
            except AttributeError:
                pass
        count = 1
        for i in searched:
            print(f"{count}. {i}")
            count += 1
        user_choice = str(input("(A to search again): "))
        if user_choice.upper() == "A":
            is_on = True

        else:
            for i in range(len(searched)):
                if int(user_choice) == i + 1:
                    temp = list(searched.values())
                    fetch(temp[i])
                    is_on = False


def fetch(url):
    title = ""
    author = ""
    status = ""
    genres = ""
    total_chapter = ""
    description = ""
    ls = []
    temp = []
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")

    try:
        div = soup.findAll('div', class_="story-info-right")
        for elements in div:
            ls.append(elements.text)
        for i in range(len(ls)):
            ls[i] = ls[i].split('\n')
        for i in ls:
            for j in i:
                if j != "":
                    temp.append(j)
                    ls = []
                    ls = temp
        title = ls[0]
        for i in range(len(ls)):
            if ls[i].startswith("Author"):
                author = ls[i + 1]
            if ls[i].startswith("Status"):
                status = ls[i + 1]
            if ls[i].startswith("Genres"):
                genres = ls[i + 1]
                genres = genres.split('-')
                for k in range(len(genres)):
                    genres[k] = genres[k]
                genres = ",".join(genres)

        # Fetching Description
        div = soup.findAll('div', class_="panel-story-info-description")
        for h3 in div:
            description = h3.text

        if len(soup.findAll('li', class_="a-h")) != 0:
            total_chapter = len(soup.findAll('li', class_="a-h"))

        else:
            total_chapter = len(soup.findAll('div', class_="row"))

        print(title)
        print(author)
        print(status)
        print(genres)
        temp = description.split("Description :")
        temp = temp[1].split('\n')
        description = temp[1]
        print(description)

        display(title, author, status, genres, description, total_chapter)

    except:
        temp_ls = []
        ul = soup.findAll('ul', class_="manga-info-text")
        for li in ul:
            temp.append(li.text)
        for i in temp:
            temp_ls = i.split('\n')
        for i in temp_ls:
            if i != "":
                ls.append(i)
        title = ls[0]
        for i in range(len(ls)):
            if ls[i].startswith("Author"):
                author = ls[i + 1]
            if ls[i].startswith("Status"):
                status = ls[i]
                status = re.search(r' \w+', status).group(0)
            if ls[i].startswith("Genres"):
                genres = ls[i + 1]
                genres = genres.split('-')
                for k in range(len(genres)):
                    genres[k] = genres[k]
                genres = ",".join(genres)

        # Fetching Description
        div = soup.findAll('div', id="noidungm")
        for i in div:
            description = i.text

        if len(soup.findAll('li', class_="a-h")) != 0:
            total_chapter = len(soup.findAll('li', class_="a-h"))

        else:
            total_chapter = len(soup.findAll('div', class_="row"))

        temp = description.split('\n')
        description = temp[2]
        print(description)
        print(title)
        print(author[:-2])
        print(status[1:])
        print(genres[:-2])

        display(title, author, status, genres, description, total_chapter)


def display(title, author, status, genres, description, total_chapter):
    print("# ------------------- Information ------------------- #")
    print()
    print(f"➤ **Title:** __{title}__")
    print(f"➤ **Other Title:** __N/A__")
    print(f"➤ **Type:** __Manga__")
    print(f"➤ **Author:** __{author}__")
    print(f"➤ **Genres:** __{genres}__")
    print(f"➤ **Status:** __{status}__")
    print()
    print(f"➤ **Synopsis:**")
    print(description)
    print()
    print(f"Total Chapters: {total_chapter}")
    time.sleep(10)


def start_mangakakalot():
    is_on = True
    while is_on:
        os.system(clear_screen())
        print("""
  __  __                         _         _         _       _   
 |  \/  |                       | |       | |       | |     | |  
 | \  / | __ _ _ __   __ _  __ _| | ____ _| | ____ _| | ___ | |_ 
 | |\/| |/ _` | '_ \ / _` |/ _` | |/ / _` | |/ / _` | |/ _ \| __|
 | |  | | (_| | | | | (_| | (_| |   < (_| |   < (_| | | (_) | |_ 
 |_|  |_|\__,_|_| |_|\__, |\__,_|_|\_\__,_|_|\_\__,_|_|\___/ \__|
                      __/ |                                      
                     |___/                                       
""")
        print("# ------------------- Welcome to Mangakakalot ------------------- #")
        print()
        print("Choose from the following:")
        print("1. Refresh the Mangalist (Not Recommended)")
        print("2. Search Mangas")
        print("B. Back")
        print("E. Exit")
        choice = str(input(": "))

        if choice.upper() == "E":
            exit()

        elif choice.upper() == "B":
            break

        elif choice == "1":
            os.system(clear_screen())
            find()

        elif choice == "2":
            os.system(clear_screen())
            search()
