import os
from urllib import response

from selenium import webdriver
from selenium.webdriver import EdgeOptions
from selenium.webdriver.common.by import By
from time import sleep
import requests
from sys import platform
from PIL import Image

def config_selenium():
    if platform == "linux" or platform == "linux2":
        edge_driver_path = f"{os.getcwd()}/MangaInfoPull/msedgewebdriver/msedgedriver"
    else:
        edge_driver_path = f"{os.getcwd()}\\MangaInfoPull\\edgedriver_win64\\msedgedriver.exe"
    options = EdgeOptions()
    options.add_argument('--log-level=3')
    options.add_argument('--headless')
    options.add_argument("--user-agent=Mozilla...")
    driver = webdriver.Edge(edge_driver_path, options=options)
    driver.implicitly_wait(0.5)

    return driver


class anilistapi:

    # return mangatitles and mangalinks and return List[List, List]
    def search_manga(manganame):

        url = f"https://anilist.co/search/manga?search={manganame}"

        driver = config_selenium()
        driver.get(url)
        sleep(1)

        mangatitles = [i.text for i in driver.find_elements(By.XPATH, "//div[@class='media-card']/a[@class='title']")]
        mangalinks = [i.get_attribute('href') for i in driver.find_elements(By.XPATH, "//div[@class='media-card']/a[@class='title']")]

        driver.quit()
        
        return [mangatitles, mangalinks]

    def get_manga_info(link):

        title = ""
        othertitle = ""
        mangatype = ""
        status = ""
        genres = ""
        author = ""
        score = ""
        popularity = ""
        description = ""

        driver = config_selenium()
        driver.get(link)
        sleep(1)

        type = [i.text for i in driver.find_elements(By.XPATH, "//div[@class='data-set']/div[@class='type']")]
        value = [i.text for i in driver.find_elements(By.XPATH, "//div[@class='data-set']/div[@class='value']")]
        type_value = dict(zip(type, value))

        title = driver.find_element(By.XPATH, "//div[@class='content']/h1").text
        for i, j in type_value.items():
            if i == "Romaji" or i == "English" or i == "Native":
                othertitle += j + ", "

            elif i == "Format":
                mangatype = j

            elif i == "Status":
                if j == "Releasing":
                    status = "Ongoing"
                elif j == "Finished":
                    status = "Completed"
                else:
                    status = j
            
            elif i == "Popularity":
                popularity = '{:,}'.format(int(j))
            
        author = driver.find_element(By.XPATH, "//div[@class='staff']/a[@class='content']/div[@class='name']").text
        value = driver.find_element(By.XPATH, "//div[@class='data-set data-list']/div[@class='value']").text
        genres = ", ".join(value.split('\n'))
        score = driver.find_element(By.XPATH, "//div[@class='el-tooltip data-set']/div[@class='value']").text
        score = score.split("%")
        score = int(score[0])/10
        description = driver.find_element(By.XPATH, "//p[@class='description']").text
        imagelink = driver.find_element(By.XPATH, "//div[@class='cover-wrap-inner']/img[@class='cover']").get_attribute('src')

        # print(title)
        # print(othertitle)
        # print(mangatype)
        # print(status)
        # print(authors)
        # print(genres)
        # print(popularity)
        # print(score)
        driver.quit()

        return [title, othertitle, mangatype, author, genres, status, score, popularity, description, imagelink]


    def show_info(self, infolist):
        choice = str(input("Do you want to download manga cover image? [y/N] "))
        if choice.lower() == 'y':
            self.get_image(infolist[1], infolist[9])
        print("Image Saved!")
        print(f"➤ **Title:** __{infolist[0]}__")
        print(f"➤ **Other Title:** __{infolist[1]}__")
        print(f"➤ **Type:** __{infolist[2]}__")
        print(f"➤ **Author:** __{infolist[3]}__")
        print(f"➤ **Genre:** __{infolist[4]}__")
        print(f"➤ **Status:** __{infolist[5]}__")
        print(f"➤ **Rating:** {infolist[6]}/10 __(scored by {infolist[7]} users)__")
        print()
        print(f"➤ **Synopsis:**\n{infolist[8]}")

    def get_image(self, manganame, imagelink):
        manganame = manganame.split(',')[0]
        response = requests.get(imagelink)
        if platform == "linux" or platform == "linux2":
            folder_name = f"{os.getcwd()}images/{manganame}/"
        else:
            folder_name = f"{os.getcwd()}\\images\\{manganame}\\"

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
            x = i + 25
            0
            cropped = im.crop((0, i, width, x))
            cropped.save(f"{folder_name}image_{count}.jpg")
            count += 1
        print(f"Images Saved! at: {folder_name}")

