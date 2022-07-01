from selenium import webdriver
from selenium.webdriver import EdgeOptions
from selenium.webdriver.common.by import By
from time import sleep
import requests
import os
from PIL import Image
from PIL import ImageFile
import json
import re
from sys import platform

ImageFile.LOAD_TRUNCATED_IMAGES = True


def clear_screen():
    if platform == "linux" or platform == "linux2":
        return "clear"
    else:
        return "cls"


if platform == "linux" or platform == "linux2":
    edge_driver_path = f"{os.getcwd()}/MangaInfoPull/msedgewebdriver/msedgedriver"
else:
    edge_driver_path = f"{os.getcwd()}\\MangaInfoPull\\edgedriver_win64\\msedgedriver.exe"


def fetch(url):
    options = EdgeOptions()
    options.headless = True
    driver = webdriver.Edge(edge_driver_path, options=options)
    # driver = webdriver.Edge(edge_driver_path)
    driver.get(url)
    sleep(3)

    title_english_author = driver.find_element(By.XPATH, "//div[@class='title sm:mx-2 sm:mb-4']").text
    title_english_author = title_english_author.split("\n")
    genres_list = driver.find_element(By.XPATH, "//div[@class='flex gap-1 flex-wrap items-center']").text.lower()
    genres_list = genres_list.split("\n")

    try:
        description = driver.find_element(By.XPATH, "//div[@class='md-md-container']").text
    except:
        description = "N/A"
    for i in range(len(genres_list)):
        if "publi" in genres_list[i]:
            try:
                genres_list[i] = genres_list[i][13:].split(',')[-1][1:].capitalize()
            except:
                genres_list[i] = genres_list[i][13:]
        genres_list[i] = genres_list[i].capitalize()
    genres_string = ""
    for i in genres_list[:-1]:
        genres_string += i + ", "

    if len(title_english_author) == 3:
        title = title_english_author[0]
        english_title = title_english_author[1]
        author = title_english_author[2]
    elif len(title_english_author) == 2:
        title = title_english_author[0]
        english_title = "N/A"
        author = title_english_author[1]

    print()
    choice = str(input("Do you want to Save the Images? (Y/N): ")).upper()
    if choice == "Y":
        image_link = driver.find_element(By.XPATH, "//img[@class='rounded shadow-md w-full h-auto']").get_attribute(
            "src")
        response = requests.get(image_link)
        if platform == "linux" or platform == "linux2":
            folder_name = f"{os.getcwd()}images/{title}/"
        else:
            folder_name = f"{os.getcwd()}\\images\\{title}\\"
        if not os.path.isdir(folder_name):
            os.makedirs(folder_name)
        image_in_folder = folder_name + "image.jpg"
        if response.status_code == 200:
            with open(os.path.join(image_in_folder), "wb") as f:
                f.write(response.content)
        im = Image.open(image_in_folder)
        width, height = im.size
        count = 0
        for i in range(0, 500, 50):
            x = i + 320
            cropped = im.crop((0, i, width, x))
            cropped.save(f"{folder_name}image_{count}.jpg")
            count += 1
        print(f"Images Saved! at: {folder_name}")

    print(f"➤ **Title:** __{title}__")
    print(f"➤ **Other Title:** __{english_title}__")
    print(f"➤ **Type:** __Manga__")
    print(f"➤ **Author:** __{author}__")
    print(f"➤ **Genres:** __{genres_string[:-2]}__")
    print(f"➤ **Status:** __{genres_list[-1]}__")
    print()
    print(f"➤ **Synopsis:**")
    print(description)
    sleep(6)
    driver.quit()


def search():
    is_on = True
    titles = {}
    searched = {}

    try:
        with open(f"{os.getcwd()}/MangaInfoPull/Mangadex/Mangadex_manga_list.json", "r") as f:
            manga_link = json.load(f)
    except:
        print("File Doesn't Exist!")
        exit()

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


def find():
    add = 0
    url = "https://mangadex.org/titles/"
    driver = webdriver.Edge(edge_driver_path)
    driver.get(url)
    sleep(5)
    last_page_list = [i.text for i in driver.find_elements(By.XPATH,
                                                           "//span[@class='flex items-center justify-center font-medium select-none']")]
    print(last_page_list)
    last_page_list_no_null = [i for i in last_page_list if i != ""]
    last_page = last_page_list_no_null[-1]
    print(last_page)
    count = 1
    title_link = {}
    titles = []
    links = []

    if os.path.exists("Mangadex_manga_list.json"):
        print("File 'Mangadex_manga_list' Already Exists")
    else:
        while count <= int(last_page):
            print(f"Page No {count}")
            titles = []
            links = []
            driver.get(f"{url}?page={count}")
            sleep(3)
            spans = driver.find_elements(By.CSS_SELECTOR, ".font-bold span")
            a = driver.find_elements(By.XPATH, "//a[@class='font-bold title']")
            titles = [i.text for i in spans]
            links = [i.get_attribute("href") for i in a]
            print(f"Total Title: {len(titles)}")
            print(f"First Manga: {titles[0]}")
            print(f"Last Manga: {titles[-1]}")
            add += len(titles)
            print(f"Total Fetched: {add}")
            print()

            if len(titles) == len(links):
                for i in range(len(titles)):
                    title_link[titles[i]] = links[i]
                count += 1
                print(f"Total Length: {len(title_link)}")
            else:
                print("Something went wrong, The length of list titles and links are not equal!")

        with open("Mangadex\\Mangadex_manga_list.json", "w") as f:
            f.write(json.dumps(title_link))
            print("File Updated!")
        print(title_link)

        sleep(10)
        driver.quit()


def info_from_link():
    url = str(input("Enter the URL: "))
    fetch(url)


def start_mangadex():
    is_on = True
    while is_on:
        os.system(clear_screen())
        print("""
  __  __                             _           
 |  \/  |                           | |          
 | \  / | __ _ _ __   __ _  __ _  __| | _____  __
 | |\/| |/ _` | '_ \ / _` |/ _` |/ _` |/ _ \ \/ /
 | |  | | (_| | | | | (_| | (_| | (_| |  __/>  < 
 |_|  |_|\__,_|_| |_|\__, |\__,_|\__,_|\___/_/\_\\
                      __/ |                      
                     |___/                       
""")
        print("# ------------------- Welcome to Mangadex ------------------- #")
        print()
        print("Choose from the following:")
        print("1. Refresh the Mangalist (Not Recommended)")
        print("2. Search Mangas")
        print("3. Get Info From a Link")
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

        elif choice == "3":
            os.system(clear_screen())
            info_from_link()
