from MangaInfoPull.Mangakakalot.mangakakalot_start import *
from MangaInfoPull.Mangadex.mangadex_start import *
from MangaInfoPull.MyAnimeList.myanimelist import *
from MangaInfoPull.AniList.anilist import *

        
def start_mangainfopull():
    is_on = True
    while is_on:
        os.system(clear_screen())
        print("""
  __  __                         _____        __      _____       _ _           
 |  \/  |                       |_   _|      / _|    |  __ \     | | |          
 | \  / | __ _ _ __   __ _  __ _  | |  _ __ | |_ ___ | |__) |   _| | | ___ _ __ 
 | |\/| |/ _` | '_ \ / _` |/ _` | | | | '_ \|  _/ _ \|  ___/ | | | | |/ _ \ '__|
 | |  | | (_| | | | | (_| | (_| |_| |_| | | | || (_) | |   | |_| | | |  __/ |   
 |_|  |_|\__,_|_| |_|\__, |\__,_|_____|_| |_|_| \___/|_|    \__,_|_|_|\___|_|   
                      __/ |                                                     
                     |___/                                                      
""")
        print("# ------------------- Manga Information Puller ------------------- #")
        print()
        print("Available Extensions")
        print("1. AniList")
        print("2. MyAnimeList")
        print("3. Mangadex")
        print("4. Mangakakalot")
        print("B. Back")
        print("E. Exit")
        choice = str(input(": "))

        if choice.upper() == "E":
            exit()

        if choice.upper() == "B":
            break

        elif choice == "1":
            start_apilist()

        elif choice == "2":
            start_myanimelist()
            
        elif choice == "3":
            start_mangadex()
        
        elif choice == "4":
            start_mangakakalot()