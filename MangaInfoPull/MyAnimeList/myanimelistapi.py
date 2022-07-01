from urllib import response
import requests
from bs4 import BeautifulSoup
import re

class myanimelistapi:

    # return titles and links of searched manga and return List[List, List]
    def search_manga(manganame):
        titles = []
        links = []
        url = f'https://myanimelist.net/manga.php?q={manganame}'
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        a = soup.find_all('a', {'class':'hoverinfo_trigger fw-b'})
        for i in a:
            titles.append(i.text)
            links.append(i['href'])

        return [titles, links]

    def get_manga_info(link):
        ls = []
        othertitle = ""
        mangatype = ""
        status = ""
        genres = ""
        authors = ""
        ratingValue = ""
        ratingCount = ""
        description = ""

        response = requests.get(link)
        soup = BeautifulSoup(response.text, "html.parser")
        title = soup.find_all('span', {'itemprop':'name'})
        title = ls.append("".join(title[-1].text.split('\n')).strip())
        title = ls[0]
        ls = []
        rightinfo = soup.find_all('div', {'class':'spaceit_pad'})
        ratingval_obj = soup.find_all('div', {'class':'spaceit_pad po-r js-statistics-info di-i'})
        description = soup.find('span', {'itemprop':'description'}).text

        for i in ratingval_obj:
            ratingValue = i.find('span', {'itemprop':'ratingValue'}).text
            ratingCount = i.find('span', {'itemprop':'ratingCount'}).text

        for i in rightinfo:
            genres_obj = i.find_all('span', {'itemprop':'genre'})
            for genre in genres_obj:
                genres = genres + genre.text + ", "
            ls.append(" ".join(i.text.split()))
    
        for i in ls:
            if i.startswith('Synonyms:') or i.startswith('Japanese:') or i.startswith('English:'):
                i = "".join(i.split(" ", 1))
                othertitle = othertitle + i.split(":", 1)[-1] + ", "
            elif i.startswith('Type:'):
                i = "".join(i.split(" ", 1))
                mangatype = i.split(":")[-1]
            elif i.startswith('Status:'):
                i = "".join(i.split(" ", 1))
                status = i.split(":")[-1]
            elif i.startswith('Authors:'):
                i = "".join(i.split(" ", 1))
                authors = i.split(":")[-1]


        # print(title)
        # print(othertitle)
        # print(mangatype)
        # print(authors)
        # print(genres)
        # print(status)
        # print(ratingValue)
        # print(ratingCount)
        # print(description)

        return [title, othertitle, mangatype, authors, genres, status, ratingValue, ratingCount, description]

    def show_info(infolist):
        print(f"➤ **Title:** __{infolist[0]}__")
        print(f"➤ **Other Title:** __{infolist[1]}__")
        print(f"➤ **Type:** __{infolist[2]}__")
        print(f"➤ **Author:** __{infolist[3]}__")
        print(f"➤ **Genre:** __{infolist[4]}__")
        print(f"➤ **Status:** __{infolist[5]}__")
        number = "{:,}".format(int(infolist[7]))
        print(f"➤ **Rating:** {infolist[6]}/10 __(scored by {number} users)__")
        print()
        print(f"➤ **Synopsis:**\n{infolist[8]}")
