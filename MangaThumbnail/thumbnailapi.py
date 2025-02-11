import os
import re
import requests

from selenium import webdriver
from selenium.webdriver import EdgeOptions
from selenium.webdriver.common.by import By
from time import sleep
from sys import platform
from PIL import Image, ImageFilter, ImageEnhance, ImageFont, ImageDraw, ImageOps


def clear_screen():
    if platform == "linux" or platform == "linux2":
        return "clear"
    else:
        return "cls"


class thumbnailapi:
    def get_thumbnail_info(self):
        os.system(clear_screen())
        print("""
  _______ _                     _                 _ _    _____                           _             
 |__   __| |                   | |               (_) |  / ____|                         | |            
    | |  | |__  _   _ _ __ ___ | |__  _ __   __ _ _| | | |  __  ___ _ __   ___ _ __ __ _| |_ ___  _ __ 
    | |  | '_ \| | | | '_ ` _ \| '_ \| '_ \ / _` | | | | | |_ |/ _ \ '_ \ / _ \ '__/ _` | __/ _ \| '__|
    | |  | | | | |_| | | | | | | |_) | | | | (_| | | | | |__| |  __/ | | |  __/ | | (_| | || (_) | |   
    |_|  |_| |_|\__,_|_| |_| |_|_.__/|_| |_|\__,_|_|_|  \_____|\___|_| |_|\___|_|  \__,_|\__\___/|_|   
                                                                                                       
                                                                                                       
""")
        print("# ------------------- Thumbnail Generator ------------------- #")
        print()
        manganame = str(input("Manga Name: "))
        mangatype = str(input("Manga Type: "))
        mangascore = str(input("Manga Score: "))
        imagelink = str(input("Manga Cover Image link: "))
        bannerimagelink = str(input("Manga Banner Image link (default [y]): "))
        if bannerimagelink == 'y':
            bannerimagelink = "https://telegra.ph/file/032fb15bf401ee878965f.png"
        startyear = str(input("Manga Start Year: "))

        self.get_image(manganame, mangatype, mangascore, imagelink, bannerimagelink, startyear)

    def get_image(self, manganame, mangatype, score, imagelink, bannerimagelink, startyear):
        manganame = re.sub(r':', "_", manganame)

        manganame_newline_ls = []

        manganame_newline = manganame
        manganame_newline_ls = manganame_newline.split('\\n')
        manganame = " ".join(manganame_newline_ls)

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
        if coverheight > emptyheight:
            while coverheight > emptyheight:
                coverwidth = int(coverwidth * 0.5)
                coverheight = int(coverheight * 0.5)
        if coverheight < emptyheight:
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

        print(titlefontsize)
        if titlefontsize > 25:
            yearfontsize = titlefontsize - 25
        
        elif titlefontsize < 25 and titlefontsize > 15:
            yearfontsize = titlefontsize -10

        elif titlefontsize < 15 and titlefontsize > 5:
            yearfontsize = titlefontsize -5

        print(yearfontsize)
        year_font = ImageFont.truetype(font_path, yearfontsize)

        ratingfontsize = 35
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
        