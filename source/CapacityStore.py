import json
import os
import re
from source._const import const
'''
capacity_table {
    "appid":appid,
    "date":2017-01-06
    "capacity":100000
}
('2016-11-24', 14681)
('2016-12-08', 15348)
('2016-12-16', 15137)
('2016-12-23', 15083)
('2016-12-29', 15029)
('2017-01-05', 16851)
92129
'''
def scanDir(dir):
    #找出类似"apps_2016_12_8"
    apps_dir = []
    for parent,dirnames,filenames in os.walk(dir):
        for dirname in dirnames:
            # print("parent is:" + parent)
            if parent==dir and re.compile("apps_\d*_\d*_*\d").match(dirname):
                apps_dir.append(const.WANDOUJIA_DIR+"/"+dirname)
    return apps_dir

def readInfoFile(infodir):
    info = json.load(open(infodir+"/info.json","r"))
    if info is None:
        print(str(infodir)+"缺少info.json文件")
        return
    return info["date"],info["count"]

app_dirs = scanDir(const.WANDOUJIA_DIR)
infos=[]
for item in app_dirs:
    infos.append(readInfoFile(item))
infos.sort(key=lambda s:s[0])
#根据日期排序
for info in infos:
    print(info)
print(sum([int(info[1])for info in infos]))