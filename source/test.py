import re

from source import MongoUtil
from source import WilsonScoreUtil

# allApps = MongoUtil.find("emotion_comment",{})
#
# datas = []
# code = 0
#
# for appinfo in allApps:
#     code += 1
#     _id = appinfo["_id"]
#     appid = appinfo["appid"]
#     comment_count = appinfo["comment_count"]
#     pos_count = appinfo["pos_count"]
#     neg_count = appinfo["neg_count"]
#     applause_rate = appinfo["applause_rate"]
#     top_score,lower_score = WilsonScoreUtil.confidence(pos_count,neg_count)
#     print(str(code)+" "+str(appid)+" top:"+str(top_score)+" lower_score:"+str(lower_score))
#
#     data = {"appid":appid,"pos_count":pos_count,"neg_count":neg_count, "applause_rate":applause_rate,"comment_count":comment_count,
#             "wilson_top_score" :top_score, "wilson_lower_score":lower_score}
#
#     # data = { "_id":id , "wilson_top_score" :top_score, "wilson_lower_score":lower_score}
#     datas.append(data)
#     MongoUtil.update("emotion_comment",{"_id":_id},data)
#
# print(len(datas))

#{'appid': ObjectId('58648f1282939b10b3d46b88'), 'wilson_lower_score': 0.3208923096194997, 'comment_count': 499, 'neg_count': 254, 'applause_rate': 0.31956521739130433, 'pos_count': 147, 'wilson_top_score': 0.4148067884968993}


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

allApps = MongoUtil.find("capacity_table",{})

datas = []
code = 0
for appinfo in allApps:
    code += 1
    _id = appinfo["_id"]
    appid = appinfo["appid"]
    date = appinfo["date"]
    capacity = appinfo["capacity"]
    capacity_num = install2num(capacity)

    data = {"_id":_id,"appid":appid,"date":date,"capacity":capacity, "capacity_num":capacity_num}
    print(data)
    datas.append(data)

MongoUtil.upsert_mary("capacity_table",datas)
print(len(datas))
#{'date': '2016-12-08', 'capacity': '3.1 万人安装', 'appid': ObjectId('58648f7d82939b10b3d4c46b'), 'capacity_num': 31000}