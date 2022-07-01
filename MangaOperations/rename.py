import os
import gc
import re
from time import sleep
from sys import platform


class Rename:
    def __init__(self, path):
        if platform == "linux" or platform == "linux2":
            self.path = path + "/"
        else:
            self.path = path + "\\"
        self.manga_name_s = os.listdir(path)

    # For Chapter Number Direct Rename Conversion
    def direct_ch_num(self):
        print(f"Will Rename, Folders: {self.manga_name_s}")
        for index, file_name in enumerate(self.manga_name_s):
            chapter_number = ""
            # If detects 'Ch' in the expression
            try:
                chapter_number = re.search(r"[Cc]h[a-zA-Z ]*[\d.a-zA-Z]*", file_name).group(0)
                chapter_number = re.sub(r'[Cc]h[a-zA-Z.]*[ ]*', 'Chapter ', chapter_number)
                chapter_number = re.sub(r'\s*- @MangaDigestion', "", chapter_number)
                for i in chapter_number:
                    if i == " ":
                        print("-", end="")
                    else:
                        print(i, end="")
                print()
                chapter_number = chapter_number + " - @MangaDigestion"
            except AttributeError:
                pass
            # If detects 'Ep' in the expression
            if chapter_number == "":
                try:
                    chapter_number = re.search(r"Ep[a-zA-Z ]*[\d.a-zA-Z]*", file_name).group(0)
                    chapter_number = re.sub(r'Ep[a-zA-Z.]*[ ]*', 'Episode ', chapter_number)
                    chapter_number = chapter_number + " - @MangaDigestion"
                except AttributeError:
                    pass
            # If detects 'Vol' in the expression
            if chapter_number == "":
                try:
                    chapter_number = re.search(r"Vol[a-zA-Z ]*[\d.a-zA-Z]*", file_name).group(0)
                    chapter_number = re.sub(r'Vol[a-zA-Z.]*[ ]*', 'Vol ', chapter_number)
                    chapter_number = chapter_number + " - @MangaDigestion"
                except AttributeError:
                    pass
            try:
                    os.rename(f"{self.path + file_name}", f"{self.path + chapter_number}")
            except:
                print("File Exists... Passing...")
            print(f"Renaming: {file_name} to {chapter_number}")
        print()
        print("Folders Renamed!")
        sleep(2)

    # For Chapter Number Parent Rename Conversion
    def parent_ch_num(self):
        print(f"Will Rename, Folders: {self.manga_name_s}")
        chapter_number = ""
        for i in self.manga_name_s:
            manga_path = self.path + i
            chapters = os.listdir(manga_path)
            for j in chapters:
                try:
                    chapter_number = re.search(r"[Cc]h[a-zA-Z ]*[\d.a-zA-Z]*", j).group(0)
                    chapter_number = re.sub(r'[Cc]h[a-zA-Z.]*[ ]*', 'Chapter ', chapter_number)
                    chapter_number = chapter_number + " - @MangaDigestion"
                except AttributeError:
                    pass
                # If detects 'Ep' in the expression
                if chapter_number == "":
                    try:
                        chapter_number = re.search(r"Ep[a-zA-Z ]*[\d.a-zA-Z]*", j).group(0)
                        chapter_number = re.sub(r'Ep[a-zA-Z.]*[ ]*', 'Episode ', chapter_number)
                        chapter_number = chapter_number + " - @MangaDigestion"
                    except AttributeError:
                        pass
                # If detects 'Vol' in the expression
                if chapter_number == "":
                    try:
                        chapter_number = re.search(r"Vol[a-zA-Z ]*[\d.a-zA-Z]*", j).group(0)
                        chapter_number = re.sub(r'Vol[a-zA-Z.]*[ ]*', 'Vol ', chapter_number)
                        chapter_number = chapter_number + " - @MangaDigestion"
                    except AttributeError:
                        pass
                # print(i)
                # print(chapter_number)
                try:
                    if platform == "linux" or platform == "linux2":
                        os.rename(f"{self.path + i}/{j}", f"{self.path + i}/{chapter_number}")
                    else:
                        os.rename(f"{self.path + i}\\{j}", f"{self.path + i}\\{chapter_number}")
                except:
                    print("File Exists... Passing...")
                print(f"Renaming: {j} to {chapter_number}")
        print()
        print("Folders Renamed!")
        sleep(2)

    def direct_ch_num_name(self):
        print(f"Will Rename, Folders: {self.manga_name_s}")
        for file_name in list(self.manga_name_s):
            chapter_num_name = ""
            # If detects 'Ch' in the expression
            try:
                chapter_num_name = re.search(r"[Cc]h[a-zA-Z. ]*\d*[a-zA-Z _',.\-()\d]*", file_name).group(0)
                chapter_num_name = re.sub(r'[Cc]h[a-zA-Z. ]*', 'Chapter ', chapter_num_name)
                chapter_num_name = chapter_num_name + " - @MangaDigestion"
            except AttributeError:
                pass
            # If detects 'Ep' in the expression
            try:
                chapter_num_name = re.search(r"Ep[a-zA-Z. ]*\d*[a-zA-Z _',.\-()\d]*", file_name).group(0)
                chapter_num_name = re.sub(r'Ep[a-zA-Z. ]*', 'Episode ', chapter_num_name)
                chapter_num_name = chapter_num_name + " - @MangaDigestion"
            except AttributeError:
                pass
            try:
                os.rename(f"{self.path + file_name}", f"{self.path + chapter_num_name}")
            except:
                print("File Exists... Passing...")
            print(f"Renaming: {file_name} to {chapter_num_name}")
        print()
        print("Folders Renamed!")
        sleep(2)

    def parent_ch_num_name(self):
        print(f"Will Rename, Folders: {self.manga_name_s}")
        chapter_num_name = ""
        for i in self.manga_name_s:
            manga_path = self.path + i
            chapters = os.listdir(manga_path)
            for j in chapters:
                try:
                    chapter_num_name = re.search(r"[Cc]h[a-zA-Z. ]*\d*[a-zA-Z _',.\-()\d]*", j).group(0)
                    chapter_num_name = re.sub(r'[Cc]h[a-zA-Z. ]*', 'Chapter ', chapter_num_name)
                    chapter_num_name = chapter_num_name + " - @MangaDigestion"
                except AttributeError:
                    pass
                # If detects 'Ep' in the expression
                try:
                    chapter_num_name = re.search(r"Ep[a-zA-Z. ]*\d*[a-zA-Z _',.\-()\d]*", j).group(0)
                    chapter_num_name = re.sub(r'Ep[a-zA-Z. ]*', 'Episode ', chapter_num_name)
                    chapter_num_name = chapter_num_name + " - @MangaDigestion"
                except AttributeError:
                    pass
                try:
                    if platform == "linux" or platform == "linux2":
                        os.rename(f"{self.path + i}/{j}", f"{self.path + i}/{chapter_num_name}")
                    else:
                        os.rename(f"{self.path + i}\\{j}", f"{self.path + i}\\{chapter_num_name}")
                except:
                    print("File Exists... Passing...")
                print(f"Renaming: {j} to {chapter_num_name}")
        print()
        print("Folders Renamed!")
        sleep(2)
