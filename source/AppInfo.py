import os
import re

from source.utils._const import const


#app信息
class AppInfo(object):
    def __init__(self,cata,name,descripe,install,url,apk):
        self.cata = cata
        #所属目录(str)
        self.name = name
        #app名字(str)
        self.descripe = descripe
        #详细的描述
        self.installnum = self.install2num(install)
        #安装人数(int)
        self.url = url
        #app url(str)
        self.apk = apk
        #apk大小(str)
        self.createCommentDir()

    #将文本转化为安装数量
    def install2num(self,install):
        result = (float)(re.findall(r"\d+\.?\d*",install)[0])
        if result==0:
            return 0
        if '亿' in install:
            result*=100000000
        if '万' in install:
            result*=10000
        return int(result)

    def createCommentDir(self):
        if not os.path.exists(const.WANDOUJIA_APPS_COMMENT_DIR+self.cata):
            os.makedirs(const.WANDOUJIA_APPS_COMMENT_DIR+self.cata)
