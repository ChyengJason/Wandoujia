import pickle

from source import MongoUtil
from source import WilsonScoreUtil
from source.Capacity import getChainIncreRateCapacity, getDowloadCapacity

'''
    capacity_rate_table{
    appid:
    date:        2016-12-29
    incre_rate:  0.1
    wilson_lower_rate: 0.01
'''

posts = []
is_not_exist = []

def getChainRateStore(appinfo):
    appid = appinfo["_id"]
    appname = appinfo["appname"]
    cataname = appinfo["catagory"]
    begin_date,end_date,app_incre = getChainIncreRateCapacity(appname,cataname)
    if app_incre is None:
        print(appname)
        file = open("../file/not_exist/not_exist_apps","a")
        is_not_exist.append(appid)
        file.write(cataname+" ")
        file.write(appname+"\n")
        file.close()
        return

    capacitys = getDowloadCapacity(appname,cataname=cataname)

    for incre in app_incre.items():
        post = {}
        post["appid"] = appid
        post["date"] = incre[0]
        post["incre_rate"] = incre[1]
        capacity = capacitys[incre[0]]
        if incre[1] <= 0:
            post["wilson_lower_rate"] = -WilsonScoreUtil.confidence_2( -incre[1],capacity)
        else:
            post["wilson_lower_rate"] = WilsonScoreUtil.confidence_2(incre[1],capacity)
        print(post)
        posts.append(post)
    MongoUtil.upsert_mary("capacity_rate_table",posts)

if __name__ == '__main__':
    appinfo_list = MongoUtil.find("app_table",{"catagory":"聊天社交"})
    for appinfo in appinfo_list:
        getChainRateStore(appinfo)

    print(len(posts))
    pickle.dump(is_not_exist, open('../file/not_exist/not_exist_appid','wb'))