import json
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
    if not MongoUtil.isExist("app_table",{"catagory":appinfo.cata,"appname":appinfo.name}):
        MongoUtil.insert("app_table",post)

    # cur = MongoUtil.find("app_table",{"catagory":appinfo.cata})
    # print([i for i in cur])

if __name__ == '__main__':
    saveAllcatasAppsToDB("apps_2017_1_5")
