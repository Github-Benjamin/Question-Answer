# -*- coding:utf-8 -*-
#  * Created by Benjamin on 2017/7/17
import MySQLdb
import time
import json

con_dict = dict(host='127.0.0.1', port=3306, user='root', passwd='', db='question', charset='utf8')

# 数据库公共函数
def InsertMysql(sql,params):
    conn = MySQLdb.connect(**con_dict)
    cursor = conn.cursor(cursorclass=MySQLdb.cursors.DictCursor)
    cursor.executemany(sql, params)
    cursor.close()
    conn.commit()
    conn.close()
    return  'Success'

def SelectMysql(sql):
    conn = MySQLdb.connect(**con_dict)
    cursor = conn.cursor(cursorclass=MySQLdb.cursors.DictCursor)
    cursor.execute(sql)
    data = cursor.fetchall()
    cursor.close()
    conn.commit()
    conn.close()
    return  data

# 查询所有的回复主题数量
def huifudata(page):
    try:
        if not page:
            page = 1
        if page <= 0:
            page = 1
        start = (int(page) - 1) * 10
    except:
        start = 0
    sql = 'SELECT * from question_content ORDER BY id DESC LIMIT %s,%s' % (start, 10)
    return SelectMysql(sql)

# 查询所有的主题数量
def titledata(page):
    try:
        if not page:
            page = 1
        if page <= 0:
            page = 1
        start = (int(page) - 1) * 10
    except:
        start = 0
    sql = 'SELECT * from question ORDER BY id DESC LIMIT %s,%s' % (start, 10)
    return SelectMysql(sql)

# 查询注册用户信息
def userdata(page):
    try:
        if not page:
            page = 1
        if page <= 0:
            page = 1
        start = (int(page) - 1) * 10
    except:
        start = 0
    sql = 'SELECT * from user ORDER BY id DESC LIMIT %s,%s' % (start, 10)
    return SelectMysql(sql)

# 页码显示规则
def PageNum(page,sqlname,apiname):
    page = int(page)
    # 计算数据总页数
    pagenum = 0
    for i in SelectMysql('SELECT * from %s'%sqlname):
        pagenum += 1
    temp = divmod(pagenum,10)
    if temp[1]==0:
        all_pagenum = temp[0]
    else:
        all_pagenum = temp[0]+1
    all_pagenum = int(all_pagenum)
    # 计算页码，选中页面标记且居中处理
    if all_pagenum<7:
        startpg = 1
        endpg = all_pagenum
    if all_pagenum>=7:
        if page<4:
            startpg = 1
            endpg = 7
        if page>=4:
            if (page+3)>all_pagenum:
                startpg = all_pagenum-6
                endpg = all_pagenum
            else:
                startpg = page-3
                endpg = page+3
    pgup = int(page - 1)
    pgdn = int(page + 1)
    if pgup<=0:
        pgup = 1
    if pgdn>=all_pagenum:
        pgdn = all_pagenum
    # 增加页面标签
    pagedata = ''
    for i in range(startpg,endpg+1):
        if page == i:
            pagedata += ('<li class ="active"><a href="/'+apiname+'/%s">%s</a></li>' % (i, i))
        else:
            pagedata += ('<li><a href="/'+apiname+'/%s">%s</a></li>' % (i, i))
    data = '<li><a href="/'+apiname+'/%s">&laquo;</a></li>%s<li><a href="/'%(pgup,pagedata)+apiname+'/%s">&raquo;</a></li>'%(pgdn)
    return data

# 修改回帖内容
def uphuifus(id,content):
    try:
        sql = "update question_content set  content='%s' where id=%s" % (content, id)
        SelectMysql(sql)
        return 1
    except:
        return 0

# 查询单个主题、内容
def titleds(id):
    try:
        sql = "select * from question where id=%s"%(id)
        data =  SelectMysql(sql)[0]
        return json.dumps(data)
    except Exception,e:
        print e