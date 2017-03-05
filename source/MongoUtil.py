# -*- coding: utf-8 -*-
import traceback

import pymongo
from bson import Code

from source.MongoConn import MongoConn

def check_connected(conn):
    #检查是否连接成功
    if not conn.connected:
        raise(NameError, 'stat:connected Error')

def save(table, value):
    # 一次操作一条记录，根据‘_id’是否存在，决定插入或更新记录
    try:
        my_conn = MongoConn()
        check_connected(my_conn)
        my_conn.db[table].save(value)
        my_conn.disconnect()
    except Exception:
        print(traceback.format_exc())

def insert(table, value):
    # 可以使用insert直接一次性向mongoDB插入整个列表，也可以插入单条记录，但是'_id'重复会报错
    try:
        my_conn = MongoConn()
        check_connected(my_conn)
        my_conn.db[table].insert(value, continue_on_error=True)
        my_conn.disconnect()
    except Exception:
        print(traceback.format_exc())

def update(table, conditions, value, s_upsert=False, s_multi=False):
    try:
        my_conn = MongoConn()
        check_connected(my_conn)
        my_conn.db[table].update(conditions, value, upsert=s_upsert, multi=s_multi)
        my_conn.disconnect()
    except Exception:
       print(traceback.format_exc())

def upsert_mary(table, datas):
    #批量更新插入，根据‘_id’更新或插入多条记录。
    #把'_id'值不存在的记录，插入数据库。'_id'值存在，则更新记录。
    #如果更新的字段在mongo中不存在，则直接新增一个字段
    try:
        my_conn = MongoConn()
        check_connected(my_conn)
        bulk = my_conn.db[table].initialize_ordered_bulk_op()
        for data in datas:
            _id=data['_id']
            tem = {}
            for d in data.items():
                if d[0] != "_id" :
                    tem[d[0]] = d[1]
            bulk.find({'_id': _id}).upsert().update({'$set': tem})
        bulk.execute()
        my_conn.disconnect()
    except Exception:
        print(traceback.format_exc())

def upsert_one(table, data):
    #更新插入，根据‘_id’更新一条记录，如果‘_id’的值不存在，则插入一条记录
    try:
        my_conn = MongoConn()
        check_connected(my_conn)
        query = {'_id': data.get('_id','')}
        if not my_conn.db[table].find_one(query):
            my_conn.db[table].insert(data)
        else:
            data.pop('_id') #删除'_id'键
            my_conn.db[table].update(query, {'$set': data})
        my_conn.disconnect()
    except Exception:
        print(traceback.format_exc())

def find_one(table, value):
    #根据条件进行查询，返回一条记录
    try:
        my_conn = MongoConn()
        check_connected(my_conn)
        result = my_conn.db[table].find_one(value)
        my_conn.disconnect()
        return result
    except Exception:
        print(traceback.format_exc())

def find(table, value):
    #根据条件进行查询，返回所有记录
    try:
        my_conn = MongoConn()
        check_connected(my_conn)
        result = my_conn.db[table].find(value)
        my_conn.disconnect()
        return result
    except Exception:
        print(traceback.format_exc())

def isExist(table,value):
    try:
        if find(table,value).count()!=None and find(table,value).count() >0:
            return True
        return False
    except Exception:
        print(traceback.format_exc())

def remove(table,value):
    #根据条件删除数据
    try:
        if find(table,value).count()>=0:
            my_conn = MongoConn()
            check_connected(my_conn)
            result = my_conn.db[table].remove(value)
            my_conn.disconnect()
            return result
    except Exception:
        print(traceback.format_exc())

def drop_db(table):
    #删除table
    try:
        my_conn = MongoConn()
        check_connected(my_conn)
        my_conn.db[table].drop()
        my_conn.disconnect()
    except Exception:
        print(traceback.format_exc())

def select_colum(table, value, colum):
    #查询指定列的所有值
    try:
        my_conn = MongoConn()
        check_connected(my_conn)
        result = my_conn.db[table].find(value, {colum:1})
        my_conn.disconnect()
        return result
    except Exception:
        print(traceback.format_exc())

def create_index(table,colum,isUnique):
    #生成索引，isUnique表示是否是唯一索引
    try:
        my_conn = MongoConn()
        check_connected(my_conn)
        my_conn.db[table].ensure_index(colum,unique=isUnique)
        my_conn.disconnect()
    except Exception:
        print(traceback.format_exc())

def distinct_count(table,distinct_tag,value=None):
    try:
        my_conn = MongoConn()
        check_connected(my_conn)
        result = my_conn.db[table].find(value).distinct(distinct_tag)
        my_conn.disconnect()
        return result
    except Exception:
        print(traceback.format_exc())

def count(table):
    try:
        my_conn = MongoConn()
        check_connected(my_conn)
        ct = my_conn.db[table].find().count()
        my_conn.disconnect()
        return ct
    except Exception:
        print(traceback.format_exc())


def sort(table,condition,order,limit=0):
    # order 1：正序 -1：逆序
    try:
        my_conn = MongoConn()
        check_connected(my_conn)
        if order != 1:
            order = pymongo.DESCENDING
        else:
            order = pymongo.ASCENDING

        if limit <= 0:
            ct = my_conn.db[table].find().sort(condition,order)
        else:
            ct = my_conn.db[table].find().sort(condition,order).limit(limit)
        my_conn.disconnect()
        return ct
    except Exception:
        print(traceback.format_exc())

def capacity_find_most(limit = 10):
    try:
        table = "capacity_table"
        my_conn = MongoConn()
        check_connected(my_conn)
        mapper = Code('''
            function()
            {
                emit( this.appid,{ appid: this.appid, capacity_num:this.capacity_num, date:this.date} );
            }
        ''')

        reduce = Code('''
            function(key,values)
            {
                var max_capacity = 0;
                var max_date = 0;
                var max_appid = 0;
                for(var i=0; i<values.length; i++)
                {
                    if(values[i].capacity_num > max_capacity)
                    {
                        max_capacity = values[i].capacity_num;
                        max_date = values[i].date;
                        max_appid = values[i].appid;
                    }
                }
                return ({appid:max_appid,capacity_num:max_capacity,date:max_date})
            }
        ''')

        ct = my_conn.db[table].map_reduce(mapper,reduce,"result")
        result = ct.find().sort("value.capacity_num",pymongo.DESCENDING).limit(limit)
        my_conn.disconnect()
        return result
    except Exception:
        print(traceback.format_exc())