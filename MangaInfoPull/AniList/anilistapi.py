from enum import Flag
import os
import re
import requests

from selenium import webdriver
from selenium.webdriver import EdgeOptions
from selenium.webdriver.common.by import By
from time import sleep
from sys import platform, platlibdir
from PIL import Image, ImageFilter, ImageEnhance, ImageFont, ImageDraw, ImageOps, ImageChops

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
        synonyms = ""
        description = ""
        startyear = ""

        driver = config_selenium()
        driver.get(link)
        sleep(1)

        type = [i.text for i in driver.find_elements(By.XPATH, "//div[@class='data-set']/div[@class='type']")]
        value = [i.text for i in driver.find_elements(By.XPATH, "//div[@class='data-set']/div[@class='value']")]
        type_value = dict(zip(type, value))
        author = driver.find_element(By.XPATH, "//div[@class='staff']/a[@class='content']/div[@class='name']").text
        value = driver.find_element(By.XPATH, "//div[@class='data-set data-list']/div[@class='value']").text
        genres = ", ".join(value.split('\n'))
        try:
            value = driver.find_elements(By.XPATH, "//div[@class='data-set data-list']/div[@class='value']")[1].text
            synonyms = ", ".join(value.split('\n'))
        except:
            synonyms = ""
        try:
            score = driver.find_element(By.XPATH, "//div[@class='el-tooltip data-set']/div[@class='value']").text
            score = score.split("%")
            score = int(score[0])/10
        except:
            score = 0
        description = driver.find_element(By.XPATH, "//p[@class='description']").text
        imagelink = driver.find_element(By.XPATH, "//div[@class='cover-wrap-inner']/img[@class='cover']").get_attribute('src')
        try:
            bannerimagelink = driver.find_element(By.XPATH, "//div[@class='banner']").get_attribute('style')[23:-3]
        except:
            bannerimagelink = "https://telegra.ph/file/032fb15bf401ee878965f.png"

        title = driver.find_element(By.XPATH, "//div[@class='content']/h1").text
        for i, j in type_value.items():
            if i == "English" or i == "Native":
                othertitle += j + ", "

            elif i == "Format":
                if j == "Manga (South Korean)":
                    mangatype = "Manhwa"
                elif j == "Manga (Chinese)":
                    mangatype = "Manhua"
                else:
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
            
            elif i == "Mean Score":
                if score == 0:
                    score =j.split("%")
                    score = int(score[0])/10

            elif i == "Start Date":
                startyear = j.split(',')[-1]

        othertitle = othertitle + synonyms

        # print(title)
        # print(othertitle)
        # print(mangatype)
        # print(status)
        # print(authors)
        # print(genres)
        # print(popularity)
        # print(score)
        driver.quit()

        return [title, othertitle, mangatype, author, genres, status, score, popularity, description, imagelink, bannerimagelink, startyear]


    def show_info(self, infolist):
        choice = str(input("Do you want to download manga cover image? [y/N] "))
        if choice.lower() == 'y':
            self.get_image(infolist[0], infolist[2], infolist[6], infolist[9], infolist[10], infolist[11])

        print(f"➤ **Title:** __{infolist[0]}__")
        print(f"➤ **Other Title:** __{infolist[1]}__")
        print(f"➤ **Type:** __{infolist[2]}__")
        print(f"➤ **Author:** __{infolist[3]}__")
        print(f"➤ **Genre:** __{infolist[4]}__")
        print(f"➤ **Status:** __{infolist[5]}__")
        print(f"➤ **Rating:** {infolist[6]}/10 __(scored by {infolist[7]} users)__")
        print()
        print(f"➤ **Synopsis:**\n{infolist[8]}")

    def get_image(self, manganame, mangatype, score, imagelink, bannerimagelink, startyear):
        manganame = re.sub(r':', "_", manganame)

        manganame_newline_ls = []

        choice = str(input(f"Enter name that you want to display, (use \\n without space, default {manganame} [y]): "))
        if choice != 'y':
            manganame_newline = choice
            manganame_newline_ls = manganame_newline.split('\\n')
            manganame = " ".join(manganame_newline_ls)

        else:
            manganame_newline_ls.append(manganame)

        response = requests.get(imagelink)
        response1 = requests.get(bannerimagelink)

        if platform == "linux" or platform == "linux2":
            folder_name = f"{os.getcwd()}/thumbnail/{manganame}/"
        else:
            folder_name = f"{os.getcwd()}\\thumbnail\\{manganame}\\"

        if not os.path.isdir(folder_name):
            os.makedirs(folder_name)

        if response.status_code == 200:
            with open(f'{folder_name}cover.jpg', "wb") as f:
                f.write(response.content)

        if response1.status_code == 200:
            with open(f'{folder_name}banner.jpg', "wb") as f:
                f.write(response1.content)


        self.manipulate_img(folder_name, mangatype, startyear, score, manganame_newline_ls)


    def manipulate_img(self, folder_name, mangatype, startyear, score, manganame_newline_ls):

        # emptywidth = int((coverwidth * 16) / 6)
        emptywidth = 1500
        emptyheight = 720
        emptyimg = Image.new('RGB', (emptywidth, emptyheight))

        tmp_bannerimg = Image.open(f'{folder_name}banner.jpg').convert('RGBA')
        tmp_bannerwidth, tmp_bannerheight = tmp_bannerimg.size
        
        bannerimg = Image.open(f'{folder_name}banner.jpg').convert('RGBA')
        bannerwidth, bannerheight = bannerimg.size

        coverimg = Image.open(f'{folder_name}cover.jpg').convert('RGBA')
        coverwidth, coverheight = coverimg.size
        while coverheight < emptyheight:
            coverwidth = int(coverwidth * 1.1)
            coverheight = int(coverheight * 1.1)
        coverimg = coverimg.resize((coverwidth, coverheight))

        mask = Image.new("L", (coverwidth, coverheight), 0)
        sar_ver = ((50, 0),(coverwidth, 0),(coverwidth, coverheight),(0, coverheight))
        ImageDraw.Draw(mask).polygon(sar_ver, fill=255)

        while tmp_bannerheight < emptyheight:
            tmp_bannerwidth = int(tmp_bannerwidth * 1.05)
            tmp_bannerheight = int(tmp_bannerheight * 1.05)
            tmp_bannerimg = tmp_bannerimg.resize((tmp_bannerwidth, tmp_bannerheight))
        tmp_bannerimg = tmp_bannerimg.filter(ImageFilter.GaussianBlur(16))
        tmp_bannerimg = ImageEnhance.Brightness(tmp_bannerimg).enhance(0.5)
        
        while bannerheight < emptyheight:
            bannerwidth = int(bannerwidth * 1.05)
            bannerheight = int(bannerheight * 1.05)
            bannerimg = bannerimg.resize((bannerwidth, bannerheight))
        bannerimg = bannerimg.filter(ImageFilter.GaussianBlur(16))
        bannerimg = ImageEnhance.Brightness(bannerimg).enhance(0.5)


        starimg = Image.open(f'{os.getcwd()}/Assets/Image/star.png')
        starfraction = 0.03

        starimg = starimg.resize((int(starfraction*emptyimg.size[0]), int(starfraction*emptyimg.size[0])))
        
        if platform == "linux" or platform == "linux2":
            font_path = f'{os.getcwd()}/Assets/Fonts/Caviar-Dreams/Caviar_Dreams_Bold.ttf'
        else:
            font_path = f'{os.getcwd()}\\Assets\\Fonts\\Caviar-Dreams\\Caviar_Dreams_Bold.ttf'

        titlefontsize = 1
        titlefraction = 0.5

        title_font = ImageFont.truetype(font_path, titlefontsize)
        while title_font.getsize(f"{startyear} - {mangatype}")[0] < titlefraction*emptyimg.size[1]:
        # iterate until the text size is just larger than the criteria
            titlefontsize += 1
            title_font = ImageFont.truetype(font_path, titlefontsize)

        if titlefontsize > 25:
            yearfontsize = titlefontsize - 25
        
        elif titlefontsize < 25 and titlefontsize > 15:
            yearfontsize = titlefontsize -10

        elif titlefontsize < 15 and titlefontsize > 5:
            yearfontsize = titlefontsize -5

        year_font = ImageFont.truetype(font_path, yearfontsize)

        ratingfontsize = 35
        # ratingfraction = 0.05
        rating_font = ImageFont.truetype(font_path, ratingfontsize)

        print(bannerimg.size[0])
        print(bannerimg.size[1])

        flag = True
        while flag == True:
            offset = int(input("Enter banner offset: "))
            height = 0.17
            for line in manganame_newline_ls:
                ImageDraw.Draw(tmp_bannerimg).text((emptyimg.size[0] * 0.06 + abs(offset), emptyimg.size[1] * height), text=line, font=title_font)
                height += 0.09
            ImageDraw.Draw(tmp_bannerimg).text(((emptyimg.size[0] * 0.06) + abs(offset), emptyimg.size[1] * 0.13), text=f"{startyear} - {mangatype}", font=year_font)
            ImageDraw.Draw(tmp_bannerimg).text((emptyimg.size[0] * 0.1 + abs(offset), emptyimg.size[1] * 0.8), text=f"{score}/10", font=rating_font)
            ImageDraw.Draw(tmp_bannerimg).text((emptyimg.size[0] * 0.06 + abs(offset), emptyimg.size[1] * 0.9), text="@MangaDigestion", font=year_font)
            emptyimg.paste(tmp_bannerimg, (offset, 0))
            emptyimg.paste(starimg, (int(emptyimg.size[0] * 0.06), int(emptyimg.size[1] * 0.79)), mask=starimg)
            emptyimg.paste(coverimg, (emptywidth - coverwidth, 0), mask=mask)

            # emptyimg.show()
            emptyimg.save(f"{folder_name}tmp.jpg")

            choice = input("Check your image, Do you want to offset it more? [y/N]")

            if choice.lower() == "y":
                continue
            else:
                real_offset = offset
                flag = False

        height = 0.17
        for line in manganame_newline_ls:
            ImageDraw.Draw(bannerimg).text((emptyimg.size[0] * 0.06 + abs(real_offset), emptyimg.size[1] * height), text=line, font=title_font)
            height += 0.09
        ImageDraw.Draw(bannerimg).text(((emptyimg.size[0] * 0.06) + abs(real_offset), emptyimg.size[1] * 0.13), text=f"{startyear} - {mangatype}", font=year_font)
        ImageDraw.Draw(bannerimg).text((emptyimg.size[0] * 0.1 + abs(real_offset), emptyimg.size[1] * 0.8), text=f"{score}/10", font=rating_font)
        ImageDraw.Draw(bannerimg).text((emptyimg.size[0] * 0.06 + abs(real_offset), emptyimg.size[1] * 0.9), text="@MangaDigestion", font=year_font)
        emptyimg.paste(bannerimg, (real_offset, 0))
        emptyimg.paste(starimg, (int(emptyimg.size[0] * 0.06), int(emptyimg.size[1] * 0.79)), mask=starimg)
        emptyimg.paste(coverimg, (emptywidth - coverwidth, 0), mask=mask)

        # emptyimg.show()
        emptyimg.save(f"{folder_name}telecover.jpg")
        print("Real Image Saved!")
        