'''
推荐指数 = 归一化(想最近一次的增长率) * 参数A + 归一化（总下载量）* 参数B +
          归一化(好评率) * 参数C + 归一化（总评论数） * 参数D +
          偏移函数()
recommend_table:
    1.appname
    2.catagory
    3.appid
    4.capacity
    5.date
    6.capacity_rate
    7.comment_wilson_lower_score
    8.comment_count
    9.recommend_score
'''
import os

from source import CapacityStore
from source import MongoUtil
from source import Normalization
from source._const import const

last_capacity_rate_param = 0.35 # 0->1
capacity_param = 0.30 # 潜质 0 -> 100000
applause_param = 0.30 # 0->1
comment_count_param = 0.15 # 0->10000

capacity_limit = 1000


def saveFile(recommendApps, limit, date,is_force_create=True):
    file_name = "../file/recommendatory/"+date+"_recommend_No."+str(limit)
    if is_force_create ==False and os.path.exists(file_name):
        print(file_name+"已经存在")
        return
    output = open(file_name, 'w')
    code = 0
    for appinfo in recommendApps:
        code+=1
        output.write(str(code)+". {\n")
        output.write("目录名称 : "+appinfo["catagory"]+" "+appinfo["appname"]+"\n")
        output.write("编号 : "+appinfo["appid"]+"\n")
        output.write("日期 : "+appinfo["date"]+"\n")
        output.write("下载量 : "+str(appinfo["capacity"])+"\n")
        output.write("下载增长率 : "+str(appinfo["capacity_rate"])+"\n")
        output.write("评论总数 : "+str(appinfo["comment_count"])+"\n")
        output.write("好评率（置信）: "+str(appinfo["comment_wilson_lower_score"])+"\n")
        output.write("推荐指数 ： "+str(appinfo["recommend_score"])+"\n")
        output.write("}\n")
    output.close()

def getRecommendInfo(appinfo,date):
    recommend_info = {}

    capacity_info = MongoUtil.find_one("capacity_table",{"appid":appinfo["_id"],"date":date})
    if capacity_info is None:
        # print(appinfo["appname"],end=" 1\n")
        return None
    capacity_rate_info = MongoUtil.find_one("capacity_rate_table",{"appid":appinfo["_id"],"date":date})
    if capacity_rate_info is None:
        # print(appinfo["appname"],end=" 2\n")
        return None
    comment_info = MongoUtil.find_one("emotion_comment",{"appid":appinfo["_id"]})
    if comment_info is None:
        # print(appinfo["appname"],end=" 3\n")
        return None

    try:
        recommend_info["appname"] = appinfo["appname"]
        recommend_info["catagory"] = appinfo["catagory"]
        recommend_info["appid"] = appinfo["_id"]
        recommend_info["capacity"] = capacity_info["capacity_num"]
        recommend_info["date"] = date
        recommend_info["capacity_rate"] = capacity_rate_info["incre_rate"]
        recommend_info["comment_wilson_lower_score"] = comment_info["wilson_lower_score"]
        recommend_info["comment_count"] = comment_info["comment_count"]
        recommend_info["recommend_score"] = (
            getLastCapacityNormalization(recommend_info["capacity_rate"]) * last_capacity_rate_param +
            getCapacityNormalization(recommend_info["capacity"]) * capacity_param +
            getApplauseNormalization(recommend_info["comment_wilson_lower_score"])* applause_param+
            getCommentCountNormalization(recommend_info["comment_count"]) * comment_count_param+
            correct(recommend_info)
        )
    except:
        print("-->"+recommend_info["appname"])

    return recommend_info

# 修正函数
def correct(recommend_info):
    return 0

def getRecommendApps(limit=10,date = "2016-12-08"):
    recommendApps = MongoUtil.sort_with_values("recommend_table",{"date":date},"recommend_score",limit=limit,order=-1)
    # recommendAppsToShow = recommendApps[:limit]
    # apps = []
    # for app in recommendApps:
    #     apps.append(app)
    #     print(app)
    # return apps
    return recommendApps

def saveRecommendApps(date):
    apps = MongoUtil.find("app_table",{})
    recommendApps = []
    tem = []
    for app in apps:
        tem.append(app)
    for app in tem:
        recommend_info = getRecommendInfo(app,date)
        if recommend_info is None:
            continue
        if MongoUtil.isExist("recommend_table",{"appid":app["_id"],"date":date}):
            print(date+" "+app["appname"]+" 已经存在")
            continue
        print(app["appname"])
        recommendApps.append(recommend_info)
    MongoUtil.upsert_mary("recommend_table",recommendApps)

def getLastCapacityNormalization(score):
    min = 0
    max = 1
    if score > max:
        score = max
    return Normalization.MaxMinNormalization(score,max,min)

def getCapacityNormalization(score):
    min = 0
    max = 100000
    if score > max:
        score = max
    return Normalization.MaxMinNormalization(score,max,min)

def getApplauseNormalization(score):
    min = 0
    max = 1
    if score > max:
        score = max
    return Normalization.MaxMinNormalization(score,max,min)

def getCommentCountNormalization(score):
    min = 0
    max = 10000
    if score > max:
        score = max
    return Normalization.MaxMinNormalization(score,max,min)

def scanDateInfo():
    apps_dir = CapacityStore.scanDir(const.WANDOUJIA_DIR)
    for app_dir in apps_dir:
        date,count = CapacityStore.readInfoFile(app_dir)
        print(date)
        saveRecommendApps(date)


if __name__ == '__main__':
    scanDateInfo()
    # saveRecommendApps("2016-12-08")
    # for app in getRecommendApps():
    #     print(app)
    # getRecommendApps()