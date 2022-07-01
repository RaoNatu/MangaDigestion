from bs4 import *
import time
from alive_progress import alive_bar
import requests
import os
import re


def coffee_manga_start():
    print("# ---------------------- Coffee Manga ---------------------- #")
    # Getting URL
    chapter_num_list = []

    manga_name = str(input("Enter Manga name: "))
    url = str(input("Enter URL: "))
    download_chapters(url, manga_name)


def download_chapters(url, manga_name):
    print()
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
