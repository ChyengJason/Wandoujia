'''
    app_detail_descripe{
        appid:
        wordid:
    }
'''
import json
import os
import re
import jieba

from source import MongoUtil
from source._const import const

path = "../file/apps_detail_descripe/"
stopWords = [word.strip() for word in open("stopword")]
punctuations = [word.strip("\n") for word in open("punctuation")]

posts = []

def read_descripe(catagory,appname):
    app_path = path+catagory+"/"+appname+".json"
    if os.path.exists(app_path):
        file = open(app_path,'r')
        content = str(file.read())
        # print(content)
        return content
    return None


def scan_catagory():
    catas = json.load(open(const.WANDOUJIA_CATA_JSON_FILE))
    for cata in catas:
        print(cata)
        scan_cata_app(cata)

def scan_cata_app(cata):
    posts.clear()
    results = MongoUtil.find("app_table",{"catagory":cata})
    code = 0
    apps = []
    for item in results:
        apps.append(item)
    for app in apps:
        code+=1
        posts.clear()

        print(code,end=" ")
        print(app["appname"])

        if MongoUtil.isExist("app_detail_descripe",{"appid":app["_id"]}):
            continue
        content = read_descripe(cata,app["appname"])
        if content is not None:
            delivery_words(app["_id"],content)
        print(len(posts))
        # print(posts)
        print()
        if(len(posts) > 0):
            MongoUtil.upsert_mary("app_detail_descripe",posts)

def delivery_words(appid,content):
    # 去除乱码
    content = re.compile('[\\x00-\\x08\\x0b-\\x0c\\x0e-\\x1f]').sub(' ', content)
    # 使用全模式
    seglist = jieba.cut(content,cut_all=False)
    for word in seglist:
        if word not in stopWords and word not in punctuations and word != '\n' and word!=' ' and not word.isdigit():
            post_word = {}
            post_word["word"]=word
            if not MongoUtil.isExist("word_table", post_word):
                MongoUtil.insert("word_table", post_word)

            result = MongoUtil.find_one("word_table", post_word)

            wordid = result['_id']
            if wordid==None:
                print(post_word)

            post_location ={}
            post_location["appid"]=appid
            post_location["wordid"]=wordid
            posts.append(post_location)

if __name__ == '__main__':
    scan_catagory()
    # scan_cata_app("音乐")