import json
import os
import re
import time


from source import MongoUtil
from source.AppInfo import AppInfo
from source._const import const


def saveAllcatasAppsToDB(filename):
    catas = json.load(open(const.WANDOUJIA_CATA_JSON_FILE))
    for cataname in catas:
        cataname = cataname.strip()
        catafilename = const.WANDOUJIA_DIR+filename+"/"+cataname+".json"
        saveCataAppsToDB(cataname,catafilename)

def saveCataAppsToDB(cataname,catafilename):
    apps = json.load(open(catafilename))
    print(cataname+" 总数量:"+str(len(apps)))
    for app in apps.items():
        name = app[0].strip().replace("/"," ")
        install = app[1]["install"]
        comment = app[1]["comment"]
        url = app[1]["url"]
        apk = app[1]["apk"]
        appinfo = AppInfo(cataname,name,comment,install,url,apk)
        saveAppToDB(appinfo)

def saveAppToDB(appinfo):
    post = {}
    post["catagory"]=appinfo.cata
    post["appname"]=appinfo.name
    # post["installnum"]=appinfo.installnum
    post["url"]=appinfo.url
    post["descripe"]=appinfo.descripe
    post["apk"]=appinfo.apk
    post["date"]=time.strftime('%Y-%m-%d',time.localtime(time.time()))
    # print(post)
    if not MongoUtil.isExist("app_table", {"catagory":appinfo.cata, "appname":appinfo.name}):
        MongoUtil.insert("app_table", post)
    print(appinfo.cata + appinfo.name)

def scanDir(dir):
    #找出类似"apps_2016_12_8"
    apps_dir = []
    for parent,dirnames,filenames in os.walk(dir):
        for dirname in dirnames:
            # print("parent is:" + parent)
            if parent==dir and re.compile("apps_\d*_\d*_*\d").match(dirname):
                apps_dir.append(dirname)
    return apps_dir

if __name__ == '__main__':
    # app_dirs = scanDir(const.WANDOUJIA_DIR)
    # print(app_dirs)
    # for app_dir in app_dirs:
    #     saveAllcatasAppsToDB(app_dir)

    saveAllcatasAppsToDB("apps_2017_2_18")

'''
视频 总数量:973
生活实用工具 总数量:963
聊天社交 总数量:978
音乐 总数量:906
图像 总数量:963
教育培训 总数量:980
'''
