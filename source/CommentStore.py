import json
import os

import jieba
import re
import time

from source import MongoUtil
from source.GetComment import AppInfo
from source._const import const

#将app信息存入数据库
#将评论信息整理分类存入数据库

#停用词
stopWords = [word.strip() for word in open("stopword")]
#标点符号
punctuations = [word.strip("\n") for word in open("punctuation")]

'''
    app_table:{"catagory":catagory,
               "appname":appname,
               "installnum":installnum,
               "url":url,
               "descripe":descripe,
               "apk":apk,
               "date":date}

    word_table:{"word":word}

    Wwordlocation_table:{"appid":appid,
                        "wordid":wordid,
                        "location":location}
'''

def deliveryWords(appinfo,filename):
    print(appinfo.name)
    contents = [line.strip() for line in open(filename)]
    wordlist = []
    line_num = 0
    result = MongoUtil.find_one("app_table",{"catagory":appinfo.cata,"appname":appinfo.name})
    if result==None:
        print("\""+appinfo.cata+" "+appinfo.name+"\" 未存入数据库中，请先存储")
        return
    appid = result['_id']

    result = MongoUtil.find_one(appinfo.cata,{"appid":appid})
    # result = MongoUtil.find_one("wordlocation_table",{"appid":appid})
    if result!=None:
        print("\""+appinfo.cata+" "+appinfo.name+"\" 已经分词存入数据库，不必重复")
        return

    for line in contents:
        time.sleep(0.1)
        line_num+=1
        # 去除乱码
        line = re.compile('[\\x00-\\x08\\x0b-\\x0c\\x0e-\\x1f]').sub(' ', line)
        # 使用全模式
        seglist = jieba.cut(line,cut_all=False)
        wordlist.append(seglist)
        for word in seglist:
            if word not in stopWords and word not in punctuations and word != '\n' and word!=' ' and not word.isdigit():
                # print(word,end=",")
                post_word = {}
                post_word["word"]=word
                if not MongoUtil.isExist("word_table",post_word):
                    MongoUtil.insert("word_table",post_word)

                result = MongoUtil.find_one("word_table",post_word)

                wordid = result['_id']
                if wordid==None:
                    print(post_word)
                post_location ={}
                post_location["appid"]=appid
                post_location["wordid"]=wordid
                post_location["location"]=line_num
                MongoUtil.insert(appinfo.cata,post_location)
                # MongoUtil.insert("wordlocation_table",post_location)

def saveCataCommentsDelivery(cataname,catafilename):
    print("分词目录："+cataname)
    apps = json.load(open(catafilename))
    for app in apps.items():
        name = app[0].strip().replace("/"," ")
        install = app[1]["install"]
        comment = app[1]["comment"]
        url = app[1]["url"]
        apk = app[1]["apk"]
        #生成appinfo
        appinfo = AppInfo(cataname,name,comment,install,url,apk)
        #app评论路径
        appcomment_path = const.WANDOUJIA_APPS_COMMENT_DIR+cataname+"/"+appinfo.name

        # print(appcomment_path,end=" -->")
        if not os.path.exists(appcomment_path):
           # print(appcomment_path,end=" -->")
           # print("文件不存在")
            continue
        if os.path.getsize(appcomment_path)==0:
           # print(appcomment_path,end=" -->")
           # print("文件为空")
            continue

        deliveryWords(appinfo,appcomment_path)

def saveCommentsDelivery():
    catas = json.load(open(const.WANDOUJIA_CATA_JSON_FILE))
    for cataname in catas:
        cataname = cataname.strip()
        catafilename = const.WANDOUJIA_DIR+"apps_12_16/"+cataname+".json"
        saveCataCommentsDelivery(cataname,catafilename)

def showData():
    print("总app数量："+str(MongoUtil.count("app_table")))
    locationCount = 0
    catas = json.load(open(const.WANDOUJIA_CATA_JSON_FILE))
    for cataname in catas:
        cataname = cataname.strip()
        print(cataname+" 数量："+str(MongoUtil.count(cataname)))
        locationCount += len(MongoUtil.distinct_count(cataname,"appid"))
    print("获取评论的app数量："+str(locationCount),end="\n\n")
    print("word数量："+str(MongoUtil.count("word_table")))

def showData(cataname):
    print("总app数量："+str(MongoUtil.count("app_table")))
    print("word数量："+str(MongoUtil.count("word_table")))
    appCount = MongoUtil.find("app_table",{"catagory":cataname}).count()
    print(cataname+"的 app数量: "+str(appCount))
    locationCount = 0
    cataname = cataname.strip()
    print(cataname+"的 location 数量："+str(MongoUtil.count(cataname)))
    locationCount += len(MongoUtil.distinct_count(cataname,"appid"))
    print("已获取评论的 app数量："+str(locationCount))
    print("未获取评论的 app数量："+str(appCount-locationCount))

def createDex():
    MongoUtil.create_index("app_table","appid",False)
    MongoUtil.create_index("word_table","word",False)
    catas = json.load(open(const.WANDOUJIA_CATA_JSON_FILE))
    for cataname in catas:
        cataname = cataname.strip()
        MongoUtil.create_index(cataname,"appid",False)
        MongoUtil.create_index(cataname,"wordid",False)

def deleteAppDieveryWord(cataname,appname):
    id = MongoUtil.find_one("app_table",{"appname":appname})["_id"]
    result = MongoUtil.remove(cataname,{"appid":id})
    print("已从“"+cataname+"”数据库中删除“"+appname+"”应用的分词信息")

if __name__ == '__main__':
    # saveAllcatasAppsToDB()
    # saveCommentsDelivery()
    # catas =  ["图像", "聊天社交","丽人母婴","交通导航","效率办公","系统工具","教育培训","旅游出行"]
    # cataname = "新闻阅读"
    cataname="旅游出行"
    catafilename = const.WANDOUJIA_DIR+"apps_12_16/"+cataname+".json"
    saveCataCommentsDelivery(cataname,catafilename)
    showData(cataname)
    # deleteAppDieveryWord("新闻阅读","咪咕动漫")
    # createDex()