import json
import os

import jieba
import re
import time

from source import MongoUtil
from source.GetComment import AppInfo
from source._const import const

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

def saveAllcatasAppsToDB():
    catas = json.load(open(const.WANDOUJIA_CATA_JSON_FILE))
    for cataname in catas:
        cataname = cataname.strip()
        catafilename = const.WANDOUJIA_DIR+"apps_12_16/"+cataname+".json"
        saveCataAppsToDB(cataname,catafilename)

def saveCataAppsToDB(cataname,catafilename):
    apps = json.load(open(catafilename))
    print("总数量:"+str(len(apps)))
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
    post["installnum"]=appinfo.installnum
    post["url"]=appinfo.url
    post["descripe"]=appinfo.descripe
    post["apk"]=appinfo.apk
    post["date"]=time.strftime('%Y-%m-%d',time.localtime(time.time()))
    # print(post)
    if not MongoUtil.isExist("app_table",post):
        MongoUtil.insert("app_table",post)

    cur = MongoUtil.find("app_table",{"catagory":appinfo.cata})
    print([i for i in cur])

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

    result = MongoUtil.find_one("wordlocation_table",{"appid":appid})
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
                MongoUtil.insert("wordlocation_table",post_location)

def saveCommentsDelivery():
    catas = json.load(open(const.WANDOUJIA_CATA_JSON_FILE))
    for cataname in catas:
        cataname = cataname.strip()
        catafilename = const.WANDOUJIA_DIR+"apps_12_16/"+cataname+".json"
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

def test():
    result = MongoUtil.find_one("app_table",{"appname":"陌陌"})
    appid = result["_id"]
    results = MongoUtil.find("wordlocation_table",{"appid":appid})
    for result in results:
        wordid = result["wordid"]

    # print(type(result[0]))
    # print(result["wordid"])
        rs = MongoUtil.find("word_table",{"_id":wordid})
        for r in rs:
            print(r)

def showData():
    print("总app数量："+str(MongoUtil.count("app_table")))
    result = MongoUtil.distinct_count("wordlocation_table","appid")
    print("获取评论的app数量："+str(len(result)))
    print("wordlocation数量："+str(MongoUtil.count("wordlocation_table")))
    print("word数量："+str(MongoUtil.count("word_table")))

def createDex():
    MongoUtil.create_index("app_table","appid",False)
    MongoUtil.create_index("word_table","word",False)
    MongoUtil.create_index("wordlocation_table","appid",False)
    MongoUtil.create_index("wordlocation_table","wordid",False)

if __name__ == '__main__':
    #saveAllcatasAppsToDB()
    # saveCommentsDelivery()
    showData()
    # createDex()
'''
总app数量：15721
获取评论的app数量：2622
wordlocation数量：742323
word数量：41362
'''