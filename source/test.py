import json

from source import MongoUtil

#生成一个信息文件info.json
#包括日期、app总数
from source._const import const

def new_info_json_file(count,date,filename):
    info = {}
    info["date"]=date
    info["count"]=count
    with open(const.WANDOUJIA_DIR+filename+"/info.json", 'w') as f:
            json.dump(info, f , ensure_ascii=False)

date = "2016-12-16"
filename = "apps_2016_12_16"
catas = json.load(open(const.WANDOUJIA_CATA_JSON_FILE))
count = 0
for cata in catas:
    apps = json.load(open(const.WANDOUJIA_DIR+filename+"/"+cata+".json"))
    count+=len(apps)
print(count)
new_info_json_file(count,date,filename)