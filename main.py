# This program is build to make it easier to Rename Manga Chapters and Conversion of its images files to PDF.
# Before running the program make sure to Check the PATH, Logics and at where you want to save your PDFs Chapters.
import os
from MangaOperations.mangaoperations_start import mangaoperations_start, clear_screen
from MangaInfoPull.mangainfopull_start import start_mangainfopull
from MangaDownloader.mangadownloader_start import start_mangadownloader

is_on = True

while is_on:
    os.system(clear_screen())
    print("""
  __  __                           _____  _                 _   _             
 |  \/  |                         |  __ \(_)               | | (_)            
 | \  / | __ _ _ __   __ _  __ _  | |  | |_  __ _  ___  ___| |_ _  ___  _ __  
 | |\/| |/ _` | '_ \ / _` |/ _` | | |  | | |/ _` |/ _ \/ __| __| |/ _ \| '_ \ 
 | |  | | (_| | | | | (_| | (_| | | |__| | | (_| |  __/\__ \ |_| | (_) | | | |
 |_|  |_|\__,_|_| |_|\__, |\__,_| |_____/|_|\__, |\___||___/\__|_|\___/|_| |_|
                      __/ |                  __/ |                            
                     |___/                  |___/                             
""")
    print("# ----------------------------- Manga Digestion ----------------------------- #")
    print()
    print("1. Manga Operations")
    print("2. Pull Manga Information")
    print("3. Download Mangas")
    print("E. Exit")
    choice = str(input("Enter your choice: "))

    if choice.upper() == "E":
        exit()
    elif choice == "1":
        mangaoperations_start()
    elif choice == "2":
        start_mangainfopull()
    elif choice == "3":
        start_mangadownloader()
