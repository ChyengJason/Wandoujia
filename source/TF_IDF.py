import math

from source import MongoUtil
from source import TagcloundUtil


class Searcher:
    def __init__(self,appinfo):
        self.__init__(appinfo.cata,appinfo.name)

    def __init__(self,appname,cataname=""):
        self.tf_idfdict = None
        if cataname == "":
            self.app = MongoUtil.find_one("app_table", {"appname":appname})
        else:
            self.app = MongoUtil.find_one("app_table", {"catagory":cataname, "appname":appname})

        if self.app is None:
            print("该app未存储在数据库，可能原因：查询不准确，未存储入数据库，数据未更新")
        print(self.app)
        self.worddict,self.wordcount= self.frequencyscore()
        if self.wordcount < 100:
            print("该app的评论数量过少，获取关键词将会不准确")
            return
        print("评论总数是："+str(self.wordcount))
        self.tf_idfdict = self.tf_idf()

    #归一化处理
    def normalizescores(self,scores,smallIsBetter=0):
        vsmall = 0.00001
        if smallIsBetter:
            minscore = min(scores.values())
            return dict([(u,float(minscore)/max(vsmall,l)) for (u,l) in scores.items()])
        else:
            maxscore = max(scores.values())
            if maxscore==0:maxscore=vsmall
            return dict([(u,float(c)/maxscore) for (u,c) in scores.items()])

    #使用计算词频率进行统计
    def frequencyscore(self):
        worddict = {}
        wordcount = 0
        cur = MongoUtil.find(self.app["catagory"], {"appid":self.app["_id"]})
        for locationinfo in cur:
            wordinfo = MongoUtil.find_one("word_table", {"_id":locationinfo["wordid"]})
            word = wordinfo["word"]
            worddict.setdefault(word,0)
            worddict[word]+=1
            wordcount+=1
        return worddict,wordcount

    #使用tf_idf进行统计
    def tf_idf(self):

        if self.worddict==None or len(self.worddict)==0:
            print("请初始化词频统计")
            return
        if self.wordcount < 100:
            print("该app的评论数量过少，获取关键词将会不准确")
            return

        #文档总数
        docu_count = len(MongoUtil.distinct_count(self.app["catagory"], "appid", value=None))
        #减去它本身
        docu_count-=1

        tf_idfdict = {}
        for item in self.worddict.items():
            result = MongoUtil.find_one("word_table", {"word":item[0]})
            wordid = result["_id"]
            include_count = len(MongoUtil.distinct_count(self.app["catagory"], "appid", value={"wordid":wordid}))
            #减去它本身
            include_count-=1

            # print(item[0]+"->"+str(item[1])+"  包含的总文档数"+str(include_count))
            # print(str(docu_count) + " "+str(include_count))
            if docu_count <= 0:
                docu_count = 0

            wordidf = float( math.log(docu_count / (include_count+1)))
            wordtf = float( item[1]/self.wordcount)
            tf_idfdict[item[0]] = wordtf * wordidf

        for item in tf_idfdict.items():
            print(item[0]+"    出现的次数："+str(self.worddict[item[0]])+"     tf-idf计算值："+str(item[1]))

        return tf_idfdict

    #生成词云
    def newTagClound(self,worddict,limit = 100):
        wordlist = [word for word in worddict.items()]
        wordlist.sort(key=lambda item : item[1],reverse=True)

        wordlist = wordlist[0:limit]
        for word in wordlist:
            print(word)
        TagcloundUtil.generateTagClound(self.app["appname"], wordlist)

if __name__ == '__main__':
    searcher = Searcher("QQ")
    if searcher.tf_idfdict is not None:
        searcher.newTagClound(searcher.tf_idfdict)