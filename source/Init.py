# 使用：
# 1. 查看app内容
# 2. 查看增长最快的app
# 3. 查看特定app的增长形势
# 4. 查看特定app的主要评论词
# 5. 查看特定app的评论情感

# 6. 基于威尔逊置信区间算法的排名：解决小样本问题
# 7. 基于项目内容的算法app推荐
# 附： 判定评论的积极消极情感
import pymongo

from source import MongoUtil

def readme():
    pass

def scanCatagorys():
    pass

def scanCatagory():
    pass

def scanAppInfo():
    pass

def scanAppRates():

    pass

def scanAppCommentWords():
    pass

def scanMostCapacityApps(limit=50):
    results = MongoUtil.capacity_find_most(limit=10)
    for result in results:
        result = result["value"]
        appid = result["appid"]
        appinfo = MongoUtil.find_one("app_table",{"_id":appid})
        appinfo["capacity_num"] = result["capacity_num"]
        appinfo["date"] = result["date"]
        print(appinfo)
        print()

def scanMostFastGrownApps():
    pass

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

def scanCommendatoryApps():
    pass

def judgeCommentEmotion():
    pass
