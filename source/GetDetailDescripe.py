import json
import os

import bs4
import requests
import time
from bs4 import BeautifulSoup

from source.AppInfo import AppInfo
from source._const import const


class DetailDescripe(object):
    def __init__(self,url):
        self.url = url
        self.apps_headers = {
        'user-Agent':'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:45.0) Gecko/20100101 Firefox/45.0',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language':'en-US,en;q=0.5',
        'Accept-Encoding':'gzip,deflate,br',
        'Connetion':'keep-alive'
        }

    #获取html
    def get_html(self,url):
        time.sleep(1)
        response = requests.get(url,allow_redirects=False,headers = self.apps_headers)
        if response.status_code == 200:
            return response.text
        else:
            return None

    #解析html
    def parse_html(self,html):
        if html==None:
            print("获取html失败，可能已经被删除")
            return ""

        soup = BeautifulSoup(html,"html.parser")
        soup = soup.select(".desc-info")
        if soup == None or len(soup)<=0:
            print("无详细描述")
            return ""
        soup = soup[0]

        details = soup.select(".con")[0]
        detail = ""
        for line in details:
            if type(line) == bs4.element.NavigableString:
                detail += line.string
        return detail

    def get_detail_comment(self):
        html = self.get_html(self.url)
        return self.parse_html(html)

def save_json_file(filename,contents):
# Writing JSON data
     with open(filename, 'w') as f:
           json.dump(contents,f,ensure_ascii=False)

def getCataAppsDetailDescripe(cataname,filename):
    apps = json.load(open(filename))
    print("总数量:"+str(len(apps)))

    if not os.path.exists(const.WANDOUJIA_APPS_DESC_DIR+cataname):
        os.mkdir(const.WANDOUJIA_APPS_DESC_DIR+cataname)
    num = 0
    for app in apps.items():
        num+=1
        name = app[0].strip().replace("/"," ")
        url = app[1]["url"]
        filename = const.WANDOUJIA_APPS_DESC_DIR+cataname+"/"+name+".json"
        if not os.path.exists(filename):
            print(str(num)+" "+name +"->")
            detail = DetailDescripe(url).get_detail_comment()
            print(detail)
            print()
            save_json_file(filename,detail)
        else:
            print(str(num)+" "+name +"->"+"已经存在")

def getAllCatasAppsDetailDescripe():
    catas = json.load(open(const.WANDOUJIA_CATA_JSON_FILE))
    for cataname in catas:
        cataname = cataname.strip()
        catafilename = const.WANDOUJIA_DIR+"apps_12_16/"+cataname+".json"
        getCataAppsDetailDescripe(cataname,catafilename)

if __name__ == '__main__':
    # "图像，丽人母婴，交通导航,效率办公，教育培训，新闻阅读，旅游出行,生活实用工具,生活服务，电话通讯,系统工具,美化手机，聊天社交，视频"
    # cataname = "音乐"
    # print(cataname)
    # catafilename = const.WANDOUJIA_DIR+"apps_12_16/"+cataname+".json"
    # # getCataAppsDetailDescripe(cataname,catafilename)
    getAllCatasAppsDetailDescripe()