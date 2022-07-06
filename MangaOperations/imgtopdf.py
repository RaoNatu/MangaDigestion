import os
import gc
from natsort import natsorted
from os.path import basename
from time import sleep
from zipfile import ZipFile
from sys import platform
from PIL import Image
from rename import Rename
from fpdf import FPDF
from io import BytesIO
from pathlib import Path


def complete():
    print()
    print("# ----------------------------- Completed ----------------------------- #")
    print("Images are Converted to PDFs!")
    print("Make sure to check left_out_pdfs.txt to see if some are not.")
    with open("MangaOperations/left_out_pdfs.txt", "r") as file:
        list_a = file.readlines()
        count = 1
        for i in list_a:
            print(f"{count}: {i}", end="")
            count += 1
    sleep(5)
    del list_a
    del count
    gc.collect()


def writing_exceptions(chapter_no, e, folder_name=""):
    print(f"Exception Caught at {chapter_no}")
    with open("MangaOperations/left_out_pdfs.txt", "a") as file:
        file.write(f"{chapter_no}: {e}\n")
    print(f"{folder_name} PDF conversion is completed!")
    sleep(2)
    del chapter_no
    del e
    del folder_name
    gc.collect()


def compressing_to_zip(path_name, pdf_dir, chapter_no):
    print("Converting to .zip file.")
    file_paths = []
    if platform == "linux" or platform == "linux2":
        path_name = path_name + "/" + chapter_no
    else:
        path_name = path_name + "\\" + chapter_no
    for root, directories, files in os.walk(path_name):
        for filename in files:
            filepath = os.path.join(root, filename)
            file_paths.append(filepath)
    print('Following files will be zipped:')
    for file_name in file_paths:
        print(file_name)
    with ZipFile(pdf_dir + chapter_no + ".zip", 'w') as zipF:
        for file in file_paths:
            zipF.write(file, basename(file))
    print('All files zipped successfully!')
    del file_paths
    del path_name
    gc.collect()


class ImgToPdf:
    def __init__(self, target_dir="", pdf_dir=""):
        self.path = target_dir
        self.pdf_dir = pdf_dir
        try:
            self.all_chapter_list = os.listdir(target_dir)
        except:
            pass
        self.chapter_list = []

    def pil_image(self, path: Path) -> BytesIO:
        img = Image.open(path).convert('RGB')
        try:
            membuf = BytesIO()
            suffix = path.split('.')[-1]
            suffix = "." + suffix
            if suffix == '.jpg' or suffix == '.png':
                img.save(membuf, format='jpeg')
            else:
                img.save(membuf)
        finally:
            img.close()
        del img
        del suffix
        gc.collect()
        return membuf

    def create_pdf(self, rename_para=""):
        print()
        if rename_para == "rename_chapter_num":
            if platform == "linux" or platform == "linux2":
                rename1 = Rename(self.path + '/')
            else:
                rename1 = Rename(self.path + '\\')
            rename1.direct_ch_num()
        elif rename_para == "rename_chapter_num_name":
            if platform == "linux" or platform == "linux2":
                rename1 = Rename(self.path + '/')
            else:
                rename1 = Rename(self.path + '\\')
            rename1.direct_ch_num_name()

        self.all_chapter_list = os.listdir(self.path)

        try:
            os.mkdir(self.pdf_dir)
        except FileExistsError:
            print("PDF Directory Already Exists")
            # rmtree(self.pdf_dir)
            # os.mkdir(self.pdf_dir)

        self.all_chapter_list.sort()
        print()
        print("All Chapter List: ")
        self.all_chapter_list = natsorted(self.all_chapter_list)
        print(self.all_chapter_list)

        pdf_chapter_lst = os.listdir(self.pdf_dir)
        for pdf_chapter in pdf_chapter_lst:
            if pdf_chapter[0:-4] in self.all_chapter_list:
                self.all_chapter_list.remove(pdf_chapter[0:-4])
                print(f"Skipping {pdf_chapter[0:-4]}")

        self.chapter_list = self.all_chapter_list
        print()
        print("Chapter in Queue: ")
        print(self.chapter_list)

        chapter_no = ""

        # Getting chapter folder names and from chapter_list and tapping into chapter folder to get images/pages
        # Using Pillow Module to Converting images/pages to pdfs
        for chapter in self.chapter_list:
            try:
                chapter_no = chapter
                if platform == "linux" or platform == "linux2":
                    image_path = f"{self.path}/{chapter}"
                else:
                    image_path = f"{self.path}\\{chapter}"
                pdf_output_path_and_name = f"{self.pdf_dir}{chapter}.pdf"
                list_pages = os.listdir(image_path)

                try:
                    list_pages.remove(".nomedia")
                except:
                    print(".nomedia not found, Skipping")

                print()
                print(f"Converting {chapter}")
                print(f"Sorted list of {chapter}")
                list_pages.sort()
                print(f"List Pages: {list_pages}")

                # PDF Conversion using FPDF2 

                pdf = FPDF('P', 'pt')
                for image in list_pages:
                    if platform == "linux" or platform == "linux2":
                        img_path = f'{image_path}/{image}'
                    else:
                        img_path = f'{image_path}\\{image}'
                    file = Image.open(img_path).convert('RGB')
                    width, height = file.size
                    pdf.add_page(format=(width, height))
                    img_bytes = self.pil_image(img_path)
                    pdf.image(img_bytes, 0, 0, width, height)
                    img_bytes.close()

                    del img_bytes
                    del image
                    gc.collect()

                pdf.output(pdf_output_path_and_name, "F")
                pdf.close()

                
                # PDF Conversion using PIL

                # Opening Image class and making Image Objects and setting them in dictionary
                # if platform == "linux" or platform == "linux2":
                #     img_obj_dict = {page_name: Image.open(f"{image_path}/{page_name}") for page_name in list_pages}
                # else:
                #     img_obj_dict = {page_name: Image.open(f"{image_path}\\{page_name}") for page_name in list_pages}

                # # Getting all the Image Objects and setting them in list
                # img_obj_list = [objects for page_name, objects in img_obj_dict.items()]
                # intro_image_obj = Image.open(f"{os.getcwd()}/MangaOperations/intro_img/Intro.png")
                # img_obj_list.insert(0, intro_image_obj)

                # img_obj_list_2 = []

                # # Converting the pages to rgb to avoid errors
                # for x in img_obj_list:
                #     x1 = x.convert('RGB')
                #     img_obj_list_2.append(x1)

                # # Main Logic of converting images to pdfs
                # # first_key = list(Img_Obj_dict.values())[0]
                # first_key = img_obj_list_2[0]
                # print(f"Object: {first_key}")
                # first_key.save(pdf_output_path_and_name, "PDF", resolution=100.0, save_all=True,
                #                append_images=img_obj_list_2[1:])

                print(f"Conversion of {chapter_no} completed!")
                print()
                del image_path
                del pdf_output_path_and_name
                del list_pages
                del chapter
                # del img_obj_dict
                # del img_obj_list
                # del img_obj_list_2
                # del x
                # del x1
                # del first_key
                gc.collect()
            except Exception as e:
                print(e)
                writing_exceptions(chapter_no, e)
                compressing_to_zip(self.path, self.pdf_dir, chapter_no)
                del chapter_no
                gc.collect()
                sleep(2)
        del self.chapter_list
        del self.path
        del self.all_chapter_list
        del pdf_chapter_lst
        del self.pdf_dir
        gc.collect()
        complete()

    def all_folder_pdf(self, rename_para=""):

        rename = Rename(self.path)
        if rename_para == "rename_chapter_num":
            rename.parent_ch_num()
        elif rename_para == "rename_chapter_num_name":
            rename.parent_ch_num_name()

        parent_pdf = self.path + "_pdf"
        try:
            os.mkdir(parent_pdf)
        except:
            print("PDF Parent Folder Already Exists")
        folder_name = os.listdir(self.path)
        if platform == "linux" or platform == "linux2":
            path_name = [self.path + "/" + i for i in folder_name]
            pdf_path_name = [self.path + "_pdf/" + i for i in folder_name]
            dele = "/"
        else:
            path_name = [self.path + "\\" + i for i in folder_name]
            pdf_path_name = [self.path + "_pdf\\" + i for i in folder_name]
            dele = "\\"
        pdf_dir = [i + "_pdf/" for i in pdf_path_name]

        for i in range(len(pdf_dir)):
            try:
                os.mkdir(pdf_dir[i])
            except FileExistsError:
                print()
                print("PDF Folder Already Exists")

            folder_all_chapter_list = os.listdir(path_name[i])
            folder_all_chapter_list = natsorted(folder_all_chapter_list)
            print()
            print("All Chapter List: ")
            print(folder_all_chapter_list)

            pdf_chapter_lst = os.listdir(pdf_dir[i])
            for pdf_chapter in pdf_chapter_lst:
                subpdf_ch = pdf_chapter[0:-4]
                if subpdf_ch in folder_all_chapter_list:
                    folder_all_chapter_list.remove(subpdf_ch)

            self.chapter_list = folder_all_chapter_list
            print()
            print(f"Chapter in {path_name[i].split(dele)[-1]}")
            print(self.chapter_list)

            chapter_no = ""

            # Getting chapter folder names and from chapter_list and tapping into chapter folder to get images/pages
            # Using Pillow Module to Converting images/pages to pdfs
            for chapter in self.chapter_list:
                try:
                    chapter_no = chapter
                    if platform == "linux" or platform == "linux2":
                        image_path = f"{path_name[i]}/{chapter}"
                    else:
                        image_path = f"{path_name[i]}\\{chapter}"
                    pdf_output_path_and_name = f"{pdf_dir[i]}{chapter}.pdf"
                    list_pages = os.listdir(image_path)

                    try:
                        list_pages.remove(".nomedia")
                    except:
                        pass

                    print()
                    print(f"Converting {chapter}")
                    print(f"Sorted list of {chapter}")
                    list_pages.sort()
                    print(list_pages)

                    # PDF Conversion using FPDF2 

                    pdf = FPDF('P', 'pt')
                    for image in list_pages:
                        if platform == "linux" or platform == "linux2":
                            img_path = f'{image_path}/{image}'
                        else:
                            img_path = f'{image_path}\\{image}'
                        file = Image.open(img_path).convert('RGB')
                        width, height = file.size
                        pdf.add_page(format=(width, height))
                        img_bytes = self.pil_image(img_path)
                        pdf.image(img_bytes, 0, 0, width, height)
                        img_bytes.close()

                        del img_bytes
                        del image
                        gc.collect()

                    pdf.output(pdf_output_path_and_name, "F")
                    pdf.close()

                    # PDF Conversion using PIL

                    # Opening Image class and making Image Objects and setting them in dictionary
                    # if platform == "linux" or platform == "linux2":
                    #     img_obj_dict = {page_name: Image.open(f"{image_path}/{page_name}") for page_name in list_pages}
                    # else:
                    #     img_obj_dict = {page_name: Image.open(f"{image_path}\\{page_name}") for page_name in list_pages}

                    # # Getting all the Image Objects and setting them in list
                    # img_obj_list = [objects for page_name, objects in img_obj_dict.items()]
                    # intro_imgae_obj = Image.open(f"{os.getcwd()}/MangaOperations/intro_img/Intro.png")
                    # img_obj_list.insert(0, intro_imgae_obj)

                    # img_obj_list_2 = []

                    # # Convertinfg the pages to rgb to avoid errors
                    # for x in img_obj_list:
                    #     x1 = x.convert('RGB')
                    #     img_obj_list_2.append(x1)

                    # # Main Logic of converting images to pdfs
                    # # first_key = list(Img_Obj_dict.values())[0]
                    # first_key = img_obj_list_2[0]
                    # print(f"Object: {first_key}")
                    # first_key.save(pdf_output_path_and_name, "PDF", resolution=100.0, save_all=True,
                    #                append_images=img_obj_list_2[1:])

                    print(f"Conversion of {chapter_no} completed!") 
                    print()
                    del chapter
                    del image_path
                    del pdf_output_path_and_name
                    del list_pages
                    # del img_obj_dict
                    # del img_obj_list
                    # del img_obj_list_2
                    # del first_key
                    gc.collect()
                except Exception as e:
                    writing_exceptions(chapter_no, e, folder_name[i])
                    compressing_to_zip(path_name[i], pdf_dir[i], chapter_no)
                    del chapter_no
                    gc.collect()

        del chapter_no
        del folder_all_chapter_list
        del self.chapter_list
        del parent_pdf
        del pdf_chapter_lst
        del folder_name
        del path_name
        del pdf_path_name
        del dele
        del pdf_dir
        gc.collect()
        complete()
