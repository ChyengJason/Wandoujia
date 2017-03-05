import json
import os
import re
import time


from source import MongoUtil
from source._const import const

'''
capacity_table {
    "appid":appid,
    "date":2017-01-06
    "capacity":1万人安装
    "capacity_num":10000
}
('2016-11-24', 14681)
('2016-12-08', 15348)
('2016-12-16', 15137)
('2016-12-23', 15083)
('2016-12-29', 15029)
('2017-01-05', 16851)
92129
'''

app_not_exist = []

def scanDir(dir):
    #找出类似"apps_2016_12_8"
    apps_dir = []
    for parent,dirnames,filenames in os.walk(dir):
        for dirname in dirnames:
            # print("parent is:" + parent)
            if parent==dir and re.compile("apps_\d*_\d*_*\d").match(dirname):
                apps_dir.append(const.WANDOUJIA_DIR+dirname)
    return apps_dir

def readInfoFile(infodir):
    info = json.load(open(infodir+"/info.json","r"))
    if info is None:
        print(str(infodir)+"缺少info.json文件")
        return
    return info["date"],info["count"]

def saveAppCapacityToDB(appid,date,capacity):
    post = {"appid":appid,"date":date}
    if not MongoUtil.isExist("capacity_table", post):
        post["capacity"]=capacity
        MongoUtil.save("capacity_table", post)

def getCataAppsInfo(filename):
    print(filename)
    date,count = readInfoFile(filename)
    catas = json.load(open(const.WANDOUJIA_CATA_JSON_FILE))
    for cataname in catas:
        cataname = cataname.strip()
        catafilename = filename+"/"+cataname+".json"
        apps = json.load(open(catafilename))
        for app in apps.items():
            name = app[0].strip().replace("/"," ")
            # capacity = app
            time.sleep(0.2)
            post = {"catagory":cataname,"appname":name}
            result = MongoUtil.find_one("app_table", post)
            print("存入的app"+name)
            if result==None:
                print(cataname+"->"+name+"   ->该app未存入数据库")
                app_not_exist.append(app)
            else:
                appid = result["_id"]
                capacity = app[1]["install"]
                # capacity = install2num(capacity)
                saveAppCapacityToDB(appid,date,capacity)

#将文本转化为安装数量
def install2num(install):
    result = (float)(re.findall(r"\d+\.?\d*",install)[0])
    if result==0:
        return 0
    if '亿' in install:
        result*=100000000
    if '万' in install:
        result*=10000
    return int(result)

def saveCapacity():
    app_dirs = scanDir(const.WANDOUJIA_DIR)
    infos=[]
    for file in app_dirs:
        getCataAppsInfo(file)
        date,count = readInfoFile(file)
        infos.append((date,count))

    infos.sort(key=lambda s:s[0])
    #根据日期排序
    for info in infos:
        print(info)

    print(sum([int(info[1])for info in infos]))

def getCapacityCount(date):
    return MongoUtil.find("capacity_table", {"date":date}).count()

# getCataAppsInfo("../file/apps_2017_1_15")
if __name__ == '__main__':
    saveCapacity()
    print("未存入的总数"+str(len(app_not_exist)))
# date = time.strptime("2016-12-29", "%Y-%m-%d")
# print(date)
# print(getCapacityCount(date))