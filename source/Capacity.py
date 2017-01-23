import datetime
import re
import time

from source.utils import FigureUtil, MongoUtil


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

def caltime(date1,date2):
    date1=time.strptime(date1,"%Y-%m-%d")
    date2=time.strptime(date2,"%Y-%m-%d")
    date1=datetime.datetime(date1[0],date1[1],date1[2],date1[3],date1[4],date1[5])
    date2=datetime.datetime(date2[0],date2[1],date2[2],date2[3],date2[4],date2[5])
    return date2-date1

def date2num(date):
    date = date.replace("-","")
    date = int(date)
    return date

def getMinAndMaxDate(datelist):
    min_date = 0
    max_date = 0
    min = 0
    max = 0
    for date in datelist:
        if min_date==0 or date2num(date)<min:
            min = date2num(date)
            min_date = date
        if max_date==0 or date2num(date)>max:
            max = date2num(date)
            max_date = date
    return min_date,max_date

def getDowloadCapacity(appname,cataname=""):
    app_capacity = {}

    capacity_table = "capacity_table"
    app_table = "app_table"
    if cataname=="":
        app = MongoUtil.find_one(app_table, {"appname":appname})
    else:
        app = MongoUtil.find_one(app_table, {"catagory":cataname, "appname":appname})
    if app ==None:
        print(cataname+appname+"不存在")
        return
    else:
        app_id = app["_id"]
        cur = MongoUtil.find(capacity_table, {"appid":app_id})
        for item in cur:
            date = item["date"]
            capacity = item["capacity"]
            if not capacity.isdigit():
                capacity = install2num(capacity)
            app_capacity[date] = capacity

    return app_capacity

def getD_ValueCapacity(appname,cataname=""):
    begin_date = 0
    d_capacity = {}

    app_capacity = getDowloadCapacity(appname,cataname=cataname)
    app_date = app_capacity.keys()
    begin_date,end_date = getMinAndMaxDate(app_date)
    for item in app_capacity.keys():
        d_capacity[caltime(begin_date,item).days] = app_capacity[item]
    return begin_date,end_date,d_capacity

def getMaxDownLoadCapacity(limit = 10):
    pass

begin_date,end_date,app_capacity = getD_ValueCapacity("小红书")
print(app_capacity)
line1 = FigureUtil.Line("xiaohongshu", app_capacity)

# begin_date,app_capacity = getD_ValueCapacity("知乎")
# print(app_capacity)
# line2 = FigureUtil.Line("zhihu",app_capacity)

graph = FigureUtil.BrokenLineChart(x_label="日期/天 (起始日期 :" + begin_date + "  到  " + end_date + ")", y_label="下载量/个")
graph.addLine(line1)
# graph.addLine(line2)
graph.showLines()