# 使用：
# 1. 查看app内容
# 2. 查看增长最快的app
# 3. 查看特定app的增长形势
# 4. 查看特定app的主要评论词
# 5. 查看特定app的评论情感
# 6. 基于威尔逊置信区间算法的排名：解决小样本问题

# 7. 查看快速增长的app
# 8. 基于项目内容的算法app推荐
# 附： 判定评论的积极消极情感
import json
import os
from source import Capacity
from source import CapacityStore
from source import Commendatory
from source import MongoUtil
from source import Nltk
from source.TF_IDF import Searcher
from source._const import const

def readme():
    txt = open("../README.md","r")
    print(txt.read())

def scanCatagorys():
    catas = json.load(open(const.WANDOUJIA_CATA_JSON_FILE))
    print("所有目录信息：")
    code = 0
    for cataname in catas:
        code+=1
        cataname = cataname.strip()
        print(str(code)+". "+cataname,end=" ")
        scanCatagoryInfo(cataname)
    print()
    count = MongoUtil.find("app_table",{}).count()
    print("总数:" + str(count))

def scanDateInfo():
    apps_dir = CapacityStore.scanDir(const.WANDOUJIA_DIR)
    for app_dir in apps_dir:
        date,count = CapacityStore.readInfoFile(app_dir)
        print(date,count)

def scanCatagoryInfo(catagory):
    count = MongoUtil.find("app_table",{"catagory":catagory}).count()
    print("app数量: "+str(count))

def scanAppInfo(appname,catagory=""):
    if catagory=="":
        apps = MongoUtil.find("app_table", {"appname":appname})
    else:
        apps = MongoUtil.find("app_table", {"catagory":catagory, "appname":appname})

    for appinfo in apps:
        print("基本信息: ")
        print(appinfo)
        catagory = appinfo["catagory"]
        dir = "../file/apps_detail_descripe/"+catagory+"/"+appinfo["appname"]+".json"

        if os.path.exists(dir):
            f = open(dir)
            print("应用描述：")
            print(f.read())
        print()

def scanChainAppRates(apps = [("知乎",""),("简书","")]):
    # apps = [("知乎",""),("简书","")]
    Capacity.showAppChainIncreRate(apps)

def scanAppCapacity(apps):
    # apps = [("知乎",""),("简书","")]
    Capacity.showAppDownLoadCapacity(apps)

def scanAppCommentWords(appname,catagory=""):
    searcher = Searcher(appname,catagory)
    if searcher.tf_idfdict is not None:
        searcher.newTagClound(searcher.tf_idfdict)

def scanMostCapacityApps(limit=50):
    results = MongoUtil.capacity_find_most(limit)
    for result in results:
        result = result["value"]
        appid = result["appid"]
        appinfo = MongoUtil.find_one("app_table",{"_id":appid})
        appinfo["capacity_num"] = result["capacity_num"]
        appinfo["date"] = result["date"]
        print(appinfo)
        print()

def scanMostFastGrownApps(order=-1,limit=50,capacity_limit = 10000,date = "2017-01-23"):
    capacity_low_limit = 10000
    results = MongoUtil.sort_with_values("capacity_rate_table",{"date":date},"incre_rate",order = order)
    for result in results:
        limit -=1
        appid = result["appid"]
        appinfo = MongoUtil.find_one("app_table",{"_id":appid})
        capacityinfo = MongoUtil.find_one("capacity_table",{"appid":appid,"date":date})
        if capacityinfo is None or capacityinfo["capacity_num"] < capacity_low_limit:
            continue
        appinfo["incre_rate"] = result["incre_rate"]
        appinfo["wilson_lower_rate"] = result["wilson_lower_rate"]
        print(appinfo)
        print()
        if limit <=0 :
            break

def scanMostPositiveApps(order=-1,limit=50):
    results = MongoUtil.sort("emotion_comment","wilson_lower_score",order = order,limit = limit)
    for result in results:
        appid = result["appid"]
        appinfo = MongoUtil.find_one("app_table",{"_id":appid})
        appinfo["comment_count"] = result["comment_count"]
        appinfo["pos_count"] = result["pos_count"]
        appinfo["neg_count"] = result["neg_count"]
        appinfo["applause_rate"] = result["applause_rate"]
        # appinfo["wilson_top_score"] = result["neg_count"]
        appinfo["wilson_lower_score"] = result["wilson_lower_score"]
        print(appinfo)
        print()

def scanCommendatoryApps(date="2016-12-08",limit=10):
    apps = Commendatory.getRecommendApps(limit=limit,date=date)
    for app in apps:
        print(app)

def judgeCommentEmotion(comment):
    Nltk.test_result(comment=comment)

if __name__ == '__main__':
    scanMostCapacityApps()
    # scanCatagoryInfo("音乐")
    # scanCatagorys()
    # scanAppInfo("QQ")
    # apps = [("知乎",""),("简书","")]
    # scanChainAppRates(apps)
    # scanMostFastGrownApps()
    # scanAppCapacity(apps)
    # scanAppCommentWords("知乎")
    # judgeCommentEmotion("很喜欢")
    # scanDateInfo()
