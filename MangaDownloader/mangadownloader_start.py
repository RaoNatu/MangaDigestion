import pandas as pd
from bs4 import *
import time
from alive_progress import alive_bar
import requests
import os
import re
from sys import platform


def clear_screen():
    if platform == "linux" or platform == "linux2":
        return "clear"
    else:
        return "cls"


def start_mangadownloader():
    is_on = True

    while is_on:
        os.system(clear_screen())
        print("""
  __  __                           _____                      _                 _           
 |  \/  |                         |  __ \                    | |               | |          
 | \  / | __ _ _ __   __ _  __ _  | |  | | _____      ___ __ | | ___   __ _  __| | ___ _ __ 
 | |\/| |/ _` | '_ \ / _` |/ _` | | |  | |/ _ \ \ /\ / / '_ \| |/ _ \ / _` |/ _` |/ _ \ '__|
 | |  | | (_| | | | | (_| | (_| | | |__| | (_) \ V  V /| | | | | (_) | (_| | (_| |  __/ |   
 |_|  |_|\__,_|_| |_|\__, |\__,_| |_____/ \___/ \_/\_/ |_| |_|_|\___/ \__,_|\__,_|\___|_|   
                      __/ |                                                                 
                     |___/                                                                  
""")
        print("# ---------------------- Welcome to MangaDownloader ---------------------- #")
        print()
        print("Choose from the following: ")
        print("1. Extensions")
        print("B. Back")
        print("E. Exit")
        choice = str(input("Enter your choice: "))

        # For Extensions
        if choice == "1":
                try:
                    with open(f'{os.getcwd()}/MangaDownloader/extensions.csv', 'r') as extensions_name:
                        print()
                        print("Available Extensions: ")
                        df = pd.read_csv(extensions_name)
                        count = df['count'].to_list()
                        website_name = df['website_name'].to_list()
                        website_link = df['website_link'].to_list()
                        method_name = df['method_name'].to_list()
                        for i in range(len(df.axes[0])):
                            print(f"{count[i]}. {website_name[i]} - {website_link[i]}")
                        choose_extension = str(input("Choose Your Extension: "))
                        for i in range(len(count)):
                            if int(choose_extension) == (i + 1):
                                method = eval(method_name[i])
                                method()
                except TypeError:
                    print("Download Complete!")
                    time.sleep(3)

        elif choice.upper() == "B":
            break

        # Exit Operation
        elif choice.upper() == "E":
            print("Exiting...")
            is_on = False

# ------------------------------------------------ Coffee Manga ------------------------------------------------ #


def coffee_manga_start():
    os.system(clear_screen())
    print("""
   _____       __  __            __  __                         
  / ____|     / _|/ _|          |  \/  |                        
 | |     ___ | |_| |_ ___  ___  | \  / | __ _ _ __   __ _  __ _ 
 | |    / _ \|  _|  _/ _ \/ _ \ | |\/| |/ _` | '_ \ / _` |/ _` |
 | |___| (_) | | | ||  __/  __/ | |  | | (_| | | | | (_| | (_| |
  \_____\___/|_| |_| \___|\___| |_|  |_|\__,_|_| |_|\__, |\__,_|
                                                     __/ |      
                                                    |___/       
""")
    print("# ---------------------- Coffee Manga ---------------------- #")
    print()
    # Getting URL
    chapter_num_list = []

    manga_name = str(input("Enter Manga name: "))
    url = str(input("Enter URL: "))
    download_chapters(url, manga_name)


def download_chapters(url, manga_name):
    os.system(clear_screen())
    print(f"# ---------------------- {manga_name} ---------------------- #")
    while True:
        print(url)
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')
        images = list(soup.findAll('img', class_="wp-manga-chapter-img"))
        chapter_number = re.search(r'chapter[-\da-zA-Z]+', url).group(0)
        try:
            print(f"Entring... {chapter_number}")
            os.makedirs(f"{manga_name}/{chapter_number}")
            chapter_path = f"{manga_name}/{chapter_number}"
        except:
            chapter_path = f"{manga_name}/{chapter_number}"
            pass
        # This Loop will loop through a single webpage
        with alive_bar(len(images)) as bar:
            for i, link in enumerate(images):
                image_link = re.search(r'https:[a-zA-Z\d\/.\-_]+', str(link)).group(0)
                # image_name = re.search(r'[\w_-]+[.](webp)', image['src'])
                # if image_name != None:
                #   image_name = image_name.group(0)
                r = requests.get(image_link).content
                image_name = re.search(r'[\w_-]+[.](webp|png|jpg|jpeg)', image_link).group(0)
                if '.webp' in image_name:
                    image_name = re.sub('webp', 'jpg', image_name)
                with open(f"{chapter_path}/{image_name}", "wb+") as f:
                    f.write(r)
                    time.sleep(0.001)
                bar()
        try:
            url = str(soup.findAll('a', class_='btn next_page')[0]['href'])
        except IndexError:
            print("All Chapters are finished!")
            print(f"Last Chapter: {chapter_number}")
            break
