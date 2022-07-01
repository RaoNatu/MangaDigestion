# This program is build to make it easier to Rename Manga Chapters and Conversion of its images files to PDF.
# Before running the program make sure to Check the PATH, Logics and at where you want to save your PDFs Chapters.
import gc
import os
import sys
import time

sys.path.append(f"{os.getcwd()}/MangaOperations")
from imgtopdf import ImgToPdf
from rename import Rename
from sys import platform
from telegram_markdown import tele_markdown


def clear_screen():
    if platform == "linux" or platform == "linux2":
        return "clear"
    else:
        return "cls"


def mangaoperations_start():
    # -------------------------- Manga Operations -------------------------- #
    is_on = True

    while is_on:

        os.system(clear_screen())

        print("""
  __  __                            ____                       _   _                 
 |  \/  |                          / __ \                     | | (_)                
 | \  / | __ _ _ __   __ _  __ _  | |  | |_ __   ___ _ __ __ _| |_ _  ___  _ __  ___ 
 | |\/| |/ _` | '_ \ / _` |/ _` | | |  | | '_ \ / _ \ '__/ _` | __| |/ _ \| '_ \/ __|
 | |  | | (_| | | | | (_| | (_| | | |__| | |_) |  __/ | | (_| | |_| | (_) | | | \__ \\
 |_|  |_|\__,_|_| |_|\__, |\__,_|  \____/| .__/ \___|_|  \__,_|\__|_|\___/|_| |_|___/
                      __/ |              | |                                         
                     |___/               |_|                                         
""")

        print("# ----------------------------- Manga Operations ----------------------------- #")
        print()
        print("1. Rename Operations")
        print("2. PDF Conversion Operations")
        print("3. Rename + PDF Operations")
        print("4. Telegram Markdown Operations")
        print("B. Back")
        print("E. Exit")

        main_choice = str(input(": "))  # Getting user choice, what to operate on selected folder
        print()

        # os.system('cls')
        if main_choice == "1":
            rename_operation_is_on = True
            while rename_operation_is_on:
                os.system(clear_screen())
                print("""
  _____                                    ____                       _   _                 
 |  __ \                                  / __ \                     | | (_)                
 | |__) |___ _ __   __ _ _ __ ___   ___  | |  | |_ __   ___ _ __ __ _| |_ _  ___  _ __  ___ 
 |  _  // _ \ '_ \ / _` | '_ ` _ \ / _ \ | |  | | '_ \ / _ \ '__/ _` | __| |/ _ \| '_ \/ __|
 | | \ \  __/ | | | (_| | | | | | |  __/ | |__| | |_) |  __/ | | (_| | |_| | (_) | | | \__ \\
 |_|  \_\___|_| |_|\__,_|_| |_| |_|\___|  \____/| .__/ \___|_|  \__,_|\__|_|\___/|_| |_|___/
                                                | |                                         
                                                |_|                                         
    """)
                print("# ----------------------------- Rename Operations ----------------------------- #")
                print()
                print("1. Rename with Chapter Number")
                print("2. Rename with Chapter Number & Name")
                print("B. Back")
                print("E. Exit")
                rename_choice = str(input(": "))

                if rename_choice == "1":
                    rename_chapter_num_is_on = True
                    while rename_chapter_num_is_on:
                        os.system(clear_screen())
                        print("""
   _____ _                 _              _   _                 _               
  / ____| |               | |            | \ | |               | |              
 | |    | |__   __ _ _ __ | |_ ___ _ __  |  \| |_   _ _ __ ___ | |__   ___ _ __ 
 | |    | '_ \ / _` | '_ \| __/ _ \ '__| | . ` | | | | '_ ` _ \| '_ \ / _ \ '__|
 | |____| | | | (_| | |_) | ||  __/ |    | |\  | |_| | | | | | | |_) |  __/ |   
  \_____|_| |_|\__,_| .__/ \__\___|_|    |_| \_|\__,_|_| |_| |_|_.__/ \___|_|   
                    | |                                                         
                    |_|                                                         
        """)
                        print()
                        print("# ----------------------------- Rename with Chapter Number ----------------------------- #")
                        print("1. Direct Rename Conversion")
                        print("2. Parent Rename Conversion")
                        print("B. Back")
                        print("E. Exit")
                        chapter_num_choice = str(input(": "))

                        # For Direct Rename Conversion
                        if chapter_num_choice == "1":
                            print("# ----------------------------- Chapter Number: Direct Rename Conversion ----------------------------- #")
                            chapter_num_rename_path = str(input("Enter the Direct Path of the Directory: "))
                            rename1 = Rename(chapter_num_rename_path)
                            manga_name_path = rename1.path[1:-1]
                            if platform == "linux" or platform == "linux2":
                                manga_name = manga_name_path.split('/')[-1]
                            else:
                                manga_name = manga_name_path.split('\\')[-1]
                            print(f"Manga Name: {manga_name}")
                            print(f"Path of the Renaming Directory: {rename1.path}")
                            choice_1 = input("Type \'Y\' to confirm the paths | Type \'N\' to choose again: ").upper()
                            if choice_1.upper() == "N":
                                pass
                                del chapter_num_choice
                                del rename1
                                del manga_name_path
                                del manga_name
                                del choice_1
                                del chapter_num_rename_path
                                gc.collect()
                            elif choice_1.upper() == "Y":
                                print()
                                rename1.direct_ch_num()
                                del chapter_num_choice
                                del rename1
                                del manga_name_path
                                del manga_name
                                del choice_1
                                del chapter_num_rename_path
                                gc.collect()

                        # For Parent Rename Conversion
                        elif chapter_num_choice == "2":
                            print("# ----------------------------- Chapter Number: Parent Rename Conversion ----------------------------- #")
                            chapter_num_rename_path = str(input("Enter the Direct Path of the Directory: "))
                            rename1 = Rename(chapter_num_rename_path)
                            manga_name_path = rename1.path[1:-1]
                            if platform == "linux" or platform == "linux2":
                                manga_name = manga_name_path.split('/')[-1]
                            else:
                                manga_name = manga_name_path.split('\\')[-1]
                            print(f"Manga Name: {manga_name}")
                            print(f"Path of the Parent Directory: {rename1.path}")
                            choice_1 = input("Type \'Y\' to confirm the paths | Type \'N\' to choose again: ").upper()
                            if choice_1.upper() == "N":
                                pass
                                del chapter_num_choice
                                del rename1
                                del manga_name_path
                                del manga_name
                                del choice_1
                                del chapter_num_rename_path
                                gc.collect()
                            elif choice_1.upper() == "Y":
                                print()
                                rename1.parent_ch_num()
                                del chapter_num_choice
                                del rename1
                                del manga_name_path
                                del manga_name
                                del choice_1
                                del chapter_num_rename_path
                                gc.collect()
                        elif chapter_num_choice.upper() == "B":
                            break
                        elif chapter_num_choice.upper() == "E":
                            exit()

                elif rename_choice == "2":
                    rename_chapter_num_name_is_on = True
                    while rename_chapter_num_name_is_on:
                        os.system(clear_screen())
                        print("""
   _____ _                 _              _   _                   _   _                      
  / ____| |               | |            | \ | |                 | \ | |                     
 | |    | |__   __ _ _ __ | |_ ___ _ __  |  \| |_   _ _ __ ___   |  \| | __ _ _ __ ___   ___ 
 | |    | '_ \ / _` | '_ \| __/ _ \ '__| | . ` | | | | '_ ` _ \  | . ` |/ _` | '_ ` _ \ / _ \\
 | |____| | | | (_| | |_) | ||  __/ |    | |\  | |_| | | | | | | | |\  | (_| | | | | | |  __/
  \_____|_| |_|\__,_| .__/ \__\___|_|    |_| \_|\__,_|_| |_| |_| |_| \_|\__,_|_| |_| |_|\___|
                    | |                                                                      
                    |_|                                                                      
""")
                        print("# ----------------------------- Rename with Chapter Number & Name ----------------------------- #")
                        print()
                        print("1. Direct Rename Conversion")
                        print("2. Parent Rename Conversion")
                        print("B. Back")
                        print("E. Exit")
                        chapter_num_name_choice = str(input(": "))

                        # Direct Chapter Num Name Conversion
                        if chapter_num_name_choice == "1":
                            print("# ----------------------------- Chapter Number & Name: Direct Rename Conversion ----------------------------- #")
                            print()
                            chapter_num_name_rename_path = str(input("Enter the Direct Path of the Directory: "))
                            rename1 = Rename(chapter_num_name_rename_path)
                            manga_name_path = rename1.path[1:-1]
                            if platform == "linux" or platform == "linux2":
                                manga_name = manga_name_path.split('/')[-1]
                            else:
                                manga_name = manga_name_path.split('\\')[-1]
                            print(f"Manga Name: {manga_name}")
                            print(f"Path of the Renaming Directory: {rename1.path}")
                            choice_1 = input("Type \'Y\' to confirm the paths | Type \'N\' to choose again: ").upper()
                            if choice_1.upper() == "N":
                                pass
                                del chapter_num_name_choice
                                del rename1
                                del manga_name_path
                                del manga_name
                                del choice_1
                                del chapter_num_name_rename_path
                                gc.collect()
                            elif choice_1.upper() == "Y":
                                print()
                                rename1.direct_ch_num_name()
                                del chapter_num_name_choice
                                del rename1
                                del manga_name_path
                                del manga_name
                                del choice_1
                                del chapter_num_name_rename_path
                                gc.collect()

                        # Direct Chapter Num Name Conversion
                        elif chapter_num_name_choice == "2":
                            print("# ----------------------------- Chapter Number & Name: Parent Rename Conversion ----------------------------- #")
                            chapter_num_name_rename_path = str(input("Enter the Direct Path of the Directory: "))
                            rename1 = Rename(chapter_num_name_rename_path)
                            manga_name_path = rename1.path[1:-1]
                            if platform == "linux" or platform == "linux2":
                                manga_name = manga_name_path.split('/')[-1]
                            else:
                                manga_name = manga_name_path.split('\\')[-1]
                            print(f"Manga Name: {manga_name}")
                            print(f"Path of the Renaming Directory: {rename1.path}")
                            choice_1 = input("Type \'Y\' to confirm the paths | Type \'N\' to choose again: ").upper()
                            if choice_1.upper() == "N":
                                pass
                                del chapter_num_name_choice
                                del rename1
                                del manga_name_path
                                del manga_name
                                del choice_1
                                del chapter_num_name_rename_path
                                gc.collect()
                            elif choice_1.upper() == "Y":
                                print()
                                rename1.parent_ch_num_name()
                                del chapter_num_name_choice
                                del rename1
                                del manga_name_path
                                del manga_name
                                del choice_1
                                del chapter_num_name_rename_path
                                gc.collect()
                        elif chapter_num_name_choice.upper() == "B":
                            break
                        elif chapter_num_name_choice.upper() == "E":
                            exit()

                elif rename_choice.upper() == "B":
                    break
                elif rename_choice.upper() == "E":
                    exit()

        # if main_choice == "1":
        #
        #     print("Selected Mode: Rename files with Chapter Number")
        #     path = str(input("Enter the path of the Directory to rename: "))
        #     rename1 = Rename(path)
        #
        #     manga_name_path = rename1.path[1:-1]
        #     if platform == "linux" or platform == "linux2":
        #         manga_name = manga_name_path.split('/')[-1]
        #     else:
        #         manga_name = manga_name_path.split('\\')[-1]
        #
        #     print()
        #     print("# ----------------------------- Renaming Folders ----------------------------- #")
        #     print(f"Manga Name: {manga_name}")
        #     print(f"Path of the Renaming Directory: {rename1.path}")
        #     file_path = ""
        #     chapter_num = ""
        #     if main_choice == "1a":
        #         print("Selected Mode: Chapter Number")
        #         file_path, chapter_num = rename1.send_sample_ch_num()
        #     if main_choice == "1b":
        #         print("Selected Mode: Chapter Number and Name")
        #         file_path, chapter_num = rename1.send_sample_ch_num_name()
        #     print(f"/////// Sample: {file_path} -> {chapter_num} ///////")
        #     print()
        #     choice_1 = input(
        #         "Type \'Y\' to confirm the paths | Type \'N\' to choose again: ").upper()
        #
        #     if choice_1 == "N":
        #         pass
        #
        #     elif choice_1 == "Y" and main_choice == "1a":
        #         print()
        #         is_on = False
        #         rename1.ch_num()
        #
        #     elif choice_1 == "Y" and main_choice == "1b":
        #         print()
        #         is_on = False
        #         rename1.ch_num_name()
        #
        #     else:
        #         print("Hmm... Something went wrong.")
        #
        # # -------------------------- Converting Images to PDF -------------------------- #
        #
        elif main_choice == "2":
            image_to_pdf_is_on = True
            while image_to_pdf_is_on:
                os.system(clear_screen())

                print("""
  _____                                   _______      _____  _____  ______ 
 |_   _|                                 |__   __|    |  __ \|  __ \|  ____|
   | |  _ __ ___   __ _  __ _  ___  ___     | | ___   | |__) | |  | | |__   
   | | | '_ ` _ \ / _` |/ _` |/ _ \/ __|    | |/ _ \  |  ___/| |  | |  __|  
  _| |_| | | | | | (_| | (_| |  __/\__ \    | | (_) | | |    | |__| | |     
 |_____|_| |_| |_|\__,_|\__, |\___||___/    |_|\___/  |_|    |_____/|_|     
                         __/ |                                              
                        |___/                                               
""")
                print("# ----------------------------- Images to PDF ----------------------------- #")
                print()
                print("1. Direct Rename Conversion")
                print("2. Parent Rename Conversion")
                print("B. Back")
                print("E. Exit")
                image_to_pdf_choice = str(input(": "))

                if image_to_pdf_choice == "1":
                    path = str(input("Enter the Direct Path of the Directory: "))
                    pdf_dir = str(input(f"Enter the path of the output directory (Y for Default-> {path}_pdf/) ")).upper()
                    if pdf_dir == "Y":
                        pdf_dir = path + "_pdf/"
                    conv1 = ImgToPdf(path, pdf_dir)
                    conv1.create_pdf()
                    del path
                    del pdf_dir
                    del conv1
                    gc.collect()

                elif image_to_pdf_choice == "2":
                    path = str(input("Enter the Direct Path of the Directory: "))
                    pdf_dir = str(
                        input(f"Enter the path of the output directory (Y for Default-> {path}_pdf/) ")).upper()
                    if pdf_dir == "Y":
                        pdf_dir = path + "_pdf/"
                    conv1 = ImgToPdf(path, pdf_dir)
                    conv1.all_folder_pdf()
                    del path
                    del pdf_dir
                    del conv1
                    gc.collect()

                elif image_to_pdf_choice.upper() == "B":
                    break
                elif image_to_pdf_choice.upper() == "E":
                    exit()

        elif main_choice == "3":
            rename_plus_pdf_is_on = True
            while rename_plus_pdf_is_on:
                os.system(clear_screen())
                print("""
  _____                                           _____  _____  ______ 
 |  __ \                                    _    |  __ \|  __ \|  ____|
 | |__) |___ _ __   __ _ _ __ ___   ___   _| |_  | |__) | |  | | |__   
 |  _  // _ \ '_ \ / _` | '_ ` _ \ / _ \ |_   _| |  ___/| |  | |  __|  
 | | \ \  __/ | | | (_| | | | | | |  __/   |_|   | |    | |__| | |     
 |_|  \_\___|_| |_|\__,_|_| |_| |_|\___|         |_|    |_____/|_|     
                                                                                                                                                  
    """)
                print("# ----------------------------- Rename + PDF ----------------------------- #")
                print()
                print("1. Rename with Chapter Number + PDF")
                print("2. Rename with Chapter Number and Name + PDF")
                print("B. Back")
                print("E. Exit")
                rename_plus_pdf_choice = str(input(": "))

                if rename_plus_pdf_choice == "1":
                    rename_plus_pdf_chapter_num_is_on = True
                    while rename_plus_pdf_chapter_num_is_on:
                        os.system(clear_screen())
                        print("""
   _____ _                 _              _   _                 _                         _____  _____  ______ 
  / ____| |               | |            | \ | |               | |                  _    |  __ \|  __ \|  ____|
 | |    | |__   __ _ _ __ | |_ ___ _ __  |  \| |_   _ _ __ ___ | |__   ___ _ __   _| |_  | |__) | |  | | |__   
 | |    | '_ \ / _` | '_ \| __/ _ \ '__| | . ` | | | | '_ ` _ \| '_ \ / _ \ '__| |_   _| |  ___/| |  | |  __|  
 | |____| | | | (_| | |_) | ||  __/ |    | |\  | |_| | | | | | | |_) |  __/ |      |_|   | |    | |__| | |     
  \_____|_| |_|\__,_| .__/ \__\___|_|    |_| \_|\__,_|_| |_| |_|_.__/ \___|_|            |_|    |_____/|_|     
                    | |                                                                                        
                    |_|                                                                                        
""")
                        print("# ----------------------------- Rename with Chapter Number + PDF ----------------------------- #")
                        print()
                        print("1. Direct Rename with Chapter Number + PDF Conversion")
                        print("2. Parent Rename with Chapter Number + PDF Conversion")
                        print("B. Back")
                        print("E. Exit")
                        choice_rename_plus_pdf = str(input(": "))

                        if choice_rename_plus_pdf == "1":
                            print()
                            path = str(input("Enter the Direct Path of the Directory: "))
                            pdf_dir = str(
                                input(f"Enter the path of the output directory (Y for Default-> {path}_pdf/) ")).upper()
                            if pdf_dir == "Y":
                                pdf_dir = path + "_pdf/"
                            conv1 = ImgToPdf(path, pdf_dir)
                            conv1.create_pdf("rename_chapter_num")
                            del path
                            del pdf_dir
                            del conv1
                            gc.collect()

                        elif choice_rename_plus_pdf == "2":
                            print()
                            path = str(input("Enter the Direct Path of the Directory: "))
                            pdf_dir = str(
                                input(f"Enter the path of the output directory (Y for Default-> {path}_pdf/) ")).upper()
                            if pdf_dir == "Y":
                                pdf_dir = path + "_pdf/"
                            conv1 = ImgToPdf(path, pdf_dir)
                            conv1.all_folder_pdf("rename_chapter_num")
                            del path
                            del pdf_dir
                            del conv1
                            gc.collect()

                        elif choice_rename_plus_pdf.upper() == "B":
                            break

                        elif choice_rename_plus_pdf.upper() == "E":
                            exit()

                elif rename_plus_pdf_choice == "2":
                    rename_plus_pdf_chapter_num_name_is_on = True
                    while rename_plus_pdf_chapter_num_name_is_on:
                        os.system(clear_screen())
                        print("""
   _____ _                 _              _   _                 _                 _   _                                _____  _____  ______ 
  / ____| |               | |            | \ | |               | |               | \ | |                         _    |  __ \|  __ \|  ____|
 | |    | |__   __ _ _ __ | |_ ___ _ __  |  \| |_   _ _ __ ___ | |__   ___ _ __  |  \| | __ _ _ __ ___   ___   _| |_  | |__) | |  | | |__   
 | |    | '_ \ / _` | '_ \| __/ _ \ '__| | . ` | | | | '_ ` _ \| '_ \ / _ \ '__| | . ` |/ _` | '_ ` _ \ / _ \ |_   _| |  ___/| |  | |  __|  
 | |____| | | | (_| | |_) | ||  __/ |    | |\  | |_| | | | | | | |_) |  __/ |    | |\  | (_| | | | | | |  __/   |_|   | |    | |__| | |     
  \_____|_| |_|\__,_| .__/ \__\___|_|    |_| \_|\__,_|_| |_| |_|_.__/ \___|_|    |_| \_|\__,_|_| |_| |_|\___|         |_|    |_____/|_|     
                    | |                                                                                                                     
                    |_|                                                                                                                     
""")
                        print("# ----------------------------- Rename with Chapter Number and Name + PDF ----------------------------- #")
                        print()
                        print("1. Direct Rename with Chapter Number + PDF Conversion")
                        print("2. Parent Rename with Chapter Number + PDF Conversion")
                        print("B. Back")
                        print("E. Exit")
                        choice_rename_plus_pdf = str(input(": "))

                        if choice_rename_plus_pdf == "1":
                            print()
                            path = str(input("Enter the Direct Path of the Directory: "))
                            pdf_dir = str(
                                input(f"Enter the path of the output directory (Y for Default-> {path}_pdf/) ")).upper()
                            if pdf_dir == "Y":
                                pdf_dir = path + "_pdf/"
                            conv1 = ImgToPdf(path, pdf_dir)
                            conv1.create_pdf("rename_chapter_num_name")
                            del path
                            del pdf_dir
                            del conv1
                            gc.collect()

                        elif choice_rename_plus_pdf == "2":
                            print()
                            path = str(input("Enter the Direct Path of the Directory: "))
                            pdf_dir = str(
                                input(f"Enter the path of the output directory (Y for Default-> {path}_pdf/) ")).upper()
                            if pdf_dir == "Y":
                                pdf_dir = path + "_pdf/"
                            conv1 = ImgToPdf(path, pdf_dir)
                            conv1.all_folder_pdf("rename_chapter_num_name")
                            del path
                            del pdf_dir
                            del conv1
                            gc.collect()

                        elif choice_rename_plus_pdf.upper() == "B":
                            break

                        elif choice_rename_plus_pdf.upper() == "E":
                            exit()

                elif rename_plus_pdf_choice.upper() == "B":
                    break

                elif rename_plus_pdf_choice.upper() == "E":
                    exit()

        elif main_choice == "4":
            os.system(clear_screen())
            print("""
  _______   _        __  __            _       _                     
 |__   __| | |      |  \/  |          | |     | |                    
    | | ___| | ___  | \  / | __ _ _ __| | ____| | _____      ___ __  
    | |/ _ \ |/ _ \ | |\/| |/ _` | '__| |/ / _` |/ _ \ \ /\ / / '_ \ 
    | |  __/ |  __/ | |  | | (_| | |  |   < (_| | (_) \ V  V /| | | |
    |_|\___|_|\___| |_|  |_|\__,_|_|  |_|\_\__,_|\___/ \_/\_/ |_| |_|
                                                                     
                                                                     
""")
            print("# ----------------------------- Images to PDF ----------------------------- #")
            print()
            path = str(input("Enter the path of the Parent Directory of PDF Folders: "))
            tele_markdown(path)
            time.sleep(10)
        elif main_choice.upper() == "B":
            break
        elif main_choice.upper() == "E":
            exit()
            # path = str(input("Enter the path of the Directory: "))
            # pdf_dir = str(input(f"Enter the path of the output directory (Y for Default-> {path}_pdf/) ")).upper()
            # if pdf_dir == "Y":
            #     pdf_dir = path + "_pdf/"
            # conv1 = ImgToPdf(path, pdf_dir)
            # conv1.create_pdf()
            # is_on = False

        # elif main_choice == "3":
        #     path = str(input("Enter the path of the Parent Directory of Folders: "))
        #     conv2 = ImgToPdf(path)
        #     conv2.all_folder_pdf()
        #     is_on = False
        #
        # elif main_choice == "4":
        #     path = str(input("Enter the path of the Parent Directory of PDF Folders: "))
        #     tele_markdown(path)
        #     is_on = False
        # elif main_choice.upper() == "B":
        #     break
        # elif main_choice.upper() == "E":
        #     exit()
        # else:
        #     print("Enter a valid choice!")
