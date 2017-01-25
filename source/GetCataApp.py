import json
import os
import random
import re
import time

import requests
from bs4 import BeautifulSoup

from source.GetCatagory import CataInfo


#获取所有app信息
class CataAppInfo(object):
    def __init__(self,cata_title,cata_url):
        self.cata_title = cata_title
        self.cata_url = cata_url
        self.cata_apps_count = 0
        self.cata_apps = {}
        self.apps_page_num = 0
        self.file_name = "../file/"+self.cata_title+".json"
        self.apps_headers = {
        'user-Agent':'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:45.0) Gecko/20100101 Firefox/45.0',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language':'en-US,en;q=0.5',
        'Accept-Encoding':'gzip,deflate,br',
        'Connetion':'keep-alive'
        }

    #获取cata_url的html
    def get_html(self):
        response = requests.get(self.cata_url,headers = self.apps_headers)
        return response.text

    #测试使用
    def open_html(self):
        f = open("../file/html4.txt","r")
        response = f.read()
        return response

    def get_apps_page_num(self,html):
        soup = BeautifulSoup(html,"html.parser")
        total_page_num = 0
        # for child in soup.html.body:nb
        #     if type(child)==bs4.element.Tag:
        #         print(child
        page_list = soup.select(".page-item")
        for page_content in page_list:
            if page_content.string.isdigit() == True and int(page_content.string) > total_page_num:
                total_page_num = int(page_content.string)
        self.apps_page_num = total_page_num

    def get_apps_content_html(self):
        if self.apps_page_num<=0:
            print("未初始化获取页数")
        else:
            for i in range(0,self.apps_page_num):
                url = self.cata_url+"_"+str(i+1)
                response = requests.get(url,headers = self.apps_headers)
                html = response.text
                self.parse_apps_content_html(html)
                time.sleep(random.randint(3,5))

        self.cata_apps_count = len(self.cata_apps)
        self.save_json_file()
        print(self.cata_title+"总数："+str(self.cata_apps_count))

    def parse_apps_content_html(self,html):
        soup = BeautifulSoup(html,"html.parser")
        info_list = soup.select(".app-desc")
        for info_soup in info_list:
            url_info = info_soup.select(".name")[0]
            install_info = info_soup.select(".install-count")[0]
            apk_info = info_soup.find('span',attrs={"title": re.compile("")})
            title = url_info["title"]
            href = url_info["href"]
            install_num = install_info.string
            apk = apk_info['title']
            comment = info_soup.select(".comment")[0].string
            detail = info_soup.select(".comment")[0].string
            app_info = {}
            app_info.setdefault("url","")
            app_info["url"]=href
            app_info.setdefault("install","")
            app_info["install"]=install_num
            app_info.setdefault("apk","")
            app_info["apk"]=apk
            app_info.setdefault("comment","")
            if comment is not None:
                app_info["comment"]=comment.strip()
            app_info.setdefault("detail","")
            if detail is not None:
                app_info["detail"]=comment.strip()
            self.cata_apps.setdefault(title,{})
            self.cata_apps[title] = app_info

    def save_json_file(self):
    # Writing JSON data
        with open(self.file_name, 'w') as f:
            json.dump(self.cata_apps, f , ensure_ascii=False)

    def load_json_file(self,title):
        self.cata_apps.clear()
        self.cata_apps_count = 0
        self.cata_apps = json.load(open(self.file_name))
        self.cata_apps_count = len(self.cata_apps)

#生成一个信息文件info.json
#包括日期、app总数
def new_info_json_file():
    count = 0
    cataInfo = CataInfo()
    cataInfo.load_json_file()
    for key in cataInfo.cata.keys():
        file_name = "../file/apps_2017_1_15/"+key+".json"
        dic = json.load(open(file_name,"r"))
        count+=len(dic)

    date = time.strftime('%Y-%m-%d',time.localtime(time.time()))
    count = count
    info = {}
    info["date"]=date
    info["count"]=count
    with open("../file/info.json", 'w') as f:
            json.dump(info, f , ensure_ascii=False)

if __name__ == '__main__':

    cataInfo = CataInfo()
    cataInfo.load_json_file()
    for key in cataInfo.cata.keys():
        file_name = "../file/"+key+".json"
        if os.path.exists(file_name):
            print(file_name)
        else:
            print("正在下载 "+key+" : "+cataInfo.cata[key])
            cataAppInfo = CataAppInfo(key,cataInfo.cata[key])
            html = cataAppInfo.get_html()
            # html = cataAppInfo.open_html()
            cataAppInfo.get_apps_page_num(html)
            cataAppInfo.get_apps_content_html()
            cataAppInfo.save_json_file()
    new_info_json_file()