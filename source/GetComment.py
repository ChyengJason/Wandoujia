import json
import os
import re
import requests
import time
import random
from bs4 import BeautifulSoup

from source.AppInfo import AppInfo
from source._const import const

#忽略下载评论的app名字
ignoreAppName = [""]
# ignoreAppName = ["Ex拨号 & 通讯录/联系人","Torque Pro (OBD2 / 汽车)","协通XT800远程控制免费版 VNC / RDP","音量助推器 / Volume Booster","Torque Pro (OBD2 / 汽车)","AV播放器(高清视频/音频版本)"]
#忽略下载评论的目录名字
# ignoreCataName = ["电话通讯","效率办公","生活服务","系统工具"]

#评论信息
class Comment(object):
    def __init__(self,appinfo):
        self.appinfo = appinfo
        self.apps_headers = {
        'user-Agent':'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:45.0) Gecko/20100101 Firefox/45.0',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language':'en-US,en;q=0.5',
        'Accept-Encoding':'gzip,deflate,br',
        'Connetion':'keep-alive'
        }

    #获取html
    def get_html(self,url):
        response = requests.get(url,headers = self.apps_headers)
        return response.text

    #解析html
    def parse_html(self,html):
        comments = []
        soup = BeautifulSoup(html,"html.parser")
        info_list = soup.select('p[class="cmt-content"]')

        if len(info_list)==0 : return True,comments
        for info in info_list:
            if info.string!=None:
                comments.append(info.string.strip())
        return False,comments

    def getCommentList(self):
        commentlist=[]
        page = 1
        isFinish=False
        while(isFinish==False):
            time.sleep(random.randint(1,2))
            url = self.appinfo.url+"/comment"+str(page)
            # print("获取评论:"+url)
            html = self.get_html(url)
            isFinish,comments = self.parse_html(html)
            if comments!=None:
                commentlist.extend(comments)
            page+=1
        return commentlist

    def isAppCommentExist(self):
        path = const.WANDOUJIA_APPS_COMMENT_DIR+self.appinfo.cata+"/"+self.appinfo.name
        if os.path.exists(path) or self.appinfo.name in ignoreAppName:
            return True
        return False

    def saveJsonFile(self,commentlist):
        with open(const.WANDOUJIA_APPS_COMMENT_DIR+self.appinfo.cata+"/"+self.appinfo.name, 'w') as f:
            for comment in commentlist:
                comment = comment.replace("\n"," ")
                f.write(comment+"\n")

def getCataAppsComment(cataname,filename):
    apps = json.load(open(filename))
    print("总数量:"+str(len(apps)))
    num = 1
    for app in apps.items():
        name = app[0].strip().replace("/"," ")
        install = app[1]["install"]
        comment = app[1]["comment"]
        url = app[1]["url"]
        apk = app[1]["apk"]
        appinfo = AppInfo(cataname,name,comment,install,url,apk)
        comment = Comment(appinfo)
        # print("序号:"+str(num)+" "+appinfo.name)
        num+=1
        if not comment.isAppCommentExist():
            commentlist = comment.getCommentList()
            comment.saveJsonFile(commentlist)
        # else:
        #     print(appinfo.name+"评论存在")

def getAllAppsComments():
    catas = json.load(open(const.WANDOUJIA_CATA_JSON_FILE))
    for cataname in catas:
    #     cataname = "视频"
        cataname = cataname.strip()
        # if cataname in ignoreCataName: continue
        if not os.path.exists(const.WANDOUJIA_APPS_COMMENT_DIR+cataname):
            print("\""+cataname+"\"文件夹不存在")
            filename = const.WANDOUJIA_DIR+"apps_12_16/"+cataname+".json"
            #获取该目录下所有app评论
            getCataAppsComment(cataname,filename)
        else:
            print("\""+cataname+"\"文件夹存在")
            filename = const.WANDOUJIA_DIR+"apps_12_16/"+cataname+".json"
            #获取该目录下所有app评论
            getCataAppsComment(cataname,filename)

    # cataname = "系统工具"
    # file = const.WANDOUJIA_DIR+"apps_12_16/"+cataname+".json"
    # getCataAppsComment(cataname,file)
# url ="http://www.wandoujia.com/apps/com.tencent.mobileqq/"
# app = AppInfo("手机通讯","QQ","descripe","1.7亿人安装",url,"3.2M")
# comment = Comment(app)
# commentlist = comment.getCommentList()
# comment.saveJsonFile(commentlist)

if __name__ == '__main__':
    getAllAppsComments()