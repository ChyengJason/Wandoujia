import datetime
import re
import time

from source import FigureUtil, MongoUtil
from source.FigureUtil import Line
from source.PinYinUtil import Pinyin

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
    if app_capacity==None:
        return
    app_date = app_capacity.keys()
    begin_date,end_date = getMinAndMaxDate(app_date)
    for item in app_capacity.keys():
        d_capacity[caltime(begin_date,item).days] = app_capacity[item]
    return begin_date,end_date,d_capacity

def getChainIncreRateCapacity(appname,cataname=""):
    #环比增长率
    rates = {}
    app_capacity = getDowloadCapacity(appname,cataname=cataname)
    if app_capacity==None:
        return None,None,None
    begin_date,end_date = getMinAndMaxDate(app_capacity.keys())

    if  len(app_capacity)<=1:
        return None,None,None

    date_list = sorted(app_capacity.keys())
    last = 0

    for i in range(1,len(date_list)):
        # print(date_list[last])
        cha = app_capacity[date_list[i]] - app_capacity[date_list[last]]
        last = i
        rates[date_list[i]] = float(cha) / (app_capacity[date_list[last]])
    # print(rates)
    return begin_date,end_date,rates

def getD_ValueChainIncreRate(appname,cataname=""):
    d_incre = {}
    begin_date,end_date,rates = getChainIncreRateCapacity(appname,cataname=cataname)

    for item in rates.keys():
        d_incre[caltime(begin_date,item).days] = rates[item]
    return begin_date,end_date,d_incre

def getMaxDownLoadCapacity(limit = 10):
    results = MongoUtil.capacity_find_most(limit)
    return results

def showD_valueAppDownLoadCapacity(apps):
    lines = []
    for app in apps:
        app_name = app[0]
        cataname = app[1]
        begin_date,end_date,app_capacity = getD_ValueCapacity(app_name,cataname)
        print(app_capacity)
        line = FigureUtil.Line(Pinyin().get_pinyin(app_name,' '), app_capacity)
        lines.append(line)

    graph = FigureUtil.LineChart(x_label="日期/天 (起始日期 :" + begin_date + "  到  " + end_date + ")", y_label="下载量/个")
    for line in lines:
        graph.addLine(line)
    graph.showLines()

def showAppDownLoadCapacity(apps):
    lines = []
    for app in apps:
        app_name = app[0]
        cataname = app[1]
        app_capacity = getDowloadCapacity(app_name,cataname)
        print(app_capacity)
        date_capacity = {}
        for date in app_capacity.keys():
            time = datetime.datetime.strptime(date,'%Y-%m-%d')
            date_capacity[time] = app_capacity[date]
        line = FigureUtil.Line(Pinyin().get_pinyin(app_name,' '), date_capacity)
        lines.append(line)

    graph = FigureUtil.LineChart(x_label="日期/天", y_label="下载量/个")
    for line in lines:
        graph.addLine(line)
    graph.showLines(is_datetime=True)

def showAppChainIncreRate(apps):
    lines = []
    values= []
    for app in apps:
        app_name = app[0]
        cataname = app[1]
        begin_date,end_date,app_incre = getChainIncreRateCapacity(app_name,cataname)
        app_capacity = getDowloadCapacity(app_name,cataname)
        print(app_capacity)
        print(app_incre)

        date_incre = {}
        for date in app_incre.keys():
            time = datetime.datetime.strptime(date,'%Y-%m-%d')
            date_incre[time] = app_incre[date]

        line = FigureUtil.Line(Pinyin().get_pinyin(app_name,' '), date_incre)
        lines.append(line)
        value = []
        for d_date in app_incre.keys():
            value.append(app_capacity[d_date])
        values.append(value)

    graph = FigureUtil.LineChart(x_label="日期/天 (起始日期 :" + begin_date + "  到  " + end_date + ")", y_label="环比增长量/%")
    for line in lines:
        graph.addLine(line)

    graph.showLines(show_value=True,values=values,is_datetime=True)

def showD_valueAppChainIncreRate(apps):

    lines = []
    values= []
    for app in apps:
        app_name = app[0]
        cataname = app[1]
        begin_date,end_date,app_incre = getD_ValueChainIncreRate(app_name,cataname)
        begin_date,end_date,app_capacity = getD_ValueCapacity(app_name,cataname)
        print(app_capacity)
        print(app_incre)
        line = FigureUtil.Line(Pinyin().get_pinyin(app_name,' '), app_incre)
        lines.append(line)
        value = []
        for d_date in app_incre.keys():
            value.append(app_capacity[d_date])
        values.append(value)

    graph = FigureUtil.LineChart(x_label="日期/天 (起始日期 :" + begin_date + "  到  " + end_date + ")", y_label="环比增长量/%")
    for line in lines:
        graph.addLine(line)

    graph.showLines(show_value=True,values=values)

if __name__ == '__main__':

# showAppDownLoadCapacity([("支付宝",""),("淘宝","购物"),("天猫","")])
# showAppChainIncreRate([("支付宝",""),("淘宝","购物"),("天猫","")])
# begin_date,end_date,d_incre = getD_ValueChainIncreRate("小红书")

# showAppDownLoadCapacity([("知乎","")])
    showAppChainIncreRate([("知乎",""),("简书","")])