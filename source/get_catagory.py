import json
import bs4
from bs4 import BeautifulSoup
from source._const import const
import requests
import datetime

class CataInfo(object):

    def __init__(self):
        self.cata_url = const.WANDOUJIA_CATA_URL
        self.cata_count = 0
        self.cata_pagenum = 0
        self.cata = {}
        self.cata_headers = {
        'user-Agent':'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:45.0) Gecko/20100101 Firefox/45.0',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language':'en-US,en;q=0.5',
        'Accept-Encoding':'gzip,deflate,br',
        'Connetion':'keep-alive'
        }

    def get_html(self):
        response = requests.get(self.cata_url,headers = self.cata_headers)
        # print(response.text)
        return response.text

    def parse_html(self,html):
        soup = BeautifulSoup(html,'html.parser')
        cata = soup.nav.ul.ul
        for child in  cata.children:
            if type(child)== bs4.element.Tag:
                child = child.a
                cata_url = child['href']
                cata_title = child['title']
                self.cata.setdefault(cata_title,cata_url)

    ##测试使用##
    def parse_file(self):
        soup = BeautifulSoup(open("../file/html.txt"),'html.parser')
        cata = soup.nav.ul.ul
        self.cata_count = 0
        for child in  cata.children:
            if type(child)== bs4.element.Tag:
                child = child.a
                cata_url = child['href']
                cata_title = child['title']
                self.cata.setdefault(cata_title,cata_url)
                self.cata_count+=1

    def save_json_file(self):
    # Writing JSON data
        with open(const.WANDOUJIA_CATA_JSON_FILE, 'w') as f:
            json.dump(self.cata, f , ensure_ascii=False)

    def load_json_file(self):
        self.cata.clear()
        self.cata = json.load(open(const.WANDOUJIA_CATA_JSON_FILE))
        self.cata_count = len(self.cata)

    def __str__(self):
        return "catagory_count: "+str(self.cata_count)+"\ncatagory: "+str(self.cata)

if __name__ == '__main__':
    cataInfo = CataInfo()
    #html = cataInfo.get_html()
    #cataInfo.parse_html(html)
    #cataInfo.parse_file()
    print(cataInfo)

    #cataInfo.save_json_file()
    cataInfo.load_json_file()
    print(cataInfo)