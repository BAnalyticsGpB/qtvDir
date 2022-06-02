import bs4
import os
from urllib import request
import re

BF_EXTENSION = "ext"
BF_TIME = "time"

REP_DATA = "Data"
URL_BISON_FUTE = "http://tipi.bison-fute.gouv.fr/bison-fute-ouvert/publicationsDIR/QTV-DIR/"

def fileNameinfo(href, filetime):
    mapInfo = {}
    # Extenion
    list_elt_href = href.split(".")
    mapInfo[BF_EXTENSION] = list_elt_href[-1]
    list_elt_time = filetime.split(" ")
    list_elt_date = list_elt_time[0].split("-")
    list_elt_heure = list_elt_time[1].split(":")
    mapInfo[BF_TIME] = list_elt_date[0] + list_elt_date[1] + list_elt_date[2]+ "_" + list_elt_heure[0] + list_elt_heure[-1]

    return mapInfo

def hasExtension(href, ext):
    list_elt_href = href.split(".")
    return list_elt_href[-1] == ext


os.makedirs(REP_DATA, exist_ok=True)

request_text = request.urlopen(URL_BISON_FUTE).read()
page = bs4.BeautifulSoup(request_text, "html.parser")

list = []
for link in page.findAll("a"): #[1:10]:
    if hasExtension(link.get("href"), "xml"):
        fileLink = link.get("href")
        # 寻找日期和时间 trouver la date et l'heure
        for tag in page.find_all('td', attrs={'align': 'right'}):
            list.append(tag.string)
        filetime = list[1]

        linkInfo = fileNameinfo(fileLink,filetime)
        path_to_save_rep = os.path.join(REP_DATA, linkInfo[BF_TIME])
        os.makedirs(path_to_save_rep, exist_ok=True)
        path_to_save_file = os.path.join(path_to_save_rep, fileLink)

        if not os.path.isfile(path_to_save_file):
            request.urlretrieve(URL_BISON_FUTE + fileLink, path_to_save_file)
            print(fileLink, " downloaded")
        else:
            print(path_to_save_file, " already exists")
