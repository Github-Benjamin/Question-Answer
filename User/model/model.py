# -*- coding:utf-8 -*-
#  * Created by Benjamin on 2017/7/17
import MySQLdb
import time
import json
from plugins import *

# import jieba

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

# 评论回复内容

def ChileContent(page):
    content = SelectMysql("select * from question_content where title_id = %s  ORDER BY id DESC" % page)
    for i in content:
        sql = "select * from content_in_content where content_id = %s"%i.get("id")
        data = SelectMysql(sql)
        if data:
            i.setdefault("ChileContent",data)
        else:
            i.setdefault("ChileContent", None)
    return json.dumps(content)

# 页码数据
def PageData(page):
    try:
        if not page:
            page = 1
        if page<=0:
            page = 1
        start = (int(page) - 1) * 5
    except :
        start = 0
    sql = 'SELECT * from question ORDER BY id DESC LIMIT %s,%s' % (start, 5)
    return SelectMysql(sql)

# 页码显示规则
def PageNum(page):
    page = int(page)
    # 计算数据总页数
    pagenum = 0
    for i in SelectMysql('SELECT * from question'):
        pagenum += 1
    temp = divmod(pagenum,5)
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
            pagedata += ('<li class ="active"><a href="/page/%s">%s</a></li>' % (i, i))
        else:
            pagedata += ('<li><a href="/page/%s">%s</a></li>' % (i, i))
    data = '''<li><a href="/page/%s">&laquo;</a></li>
              %s
              <li><a href="/page/%s">&raquo;</a></li>'''%(pgup,pagedata,pgdn)
    return data

# 搜索函数
def Searchs(kw):
    sql = "select * from question where title like '%s%s%s' or content like '%s%s%s'" % ('%', kw, '%', '%', kw, '%')
    return SelectMysql(sql)

# 用户激活操作
def Activations(email,ticket):
    sql = "select * from user where email='%s' and username='%s'"%(email,ticket)
    data = SelectMysql(sql)
    try:
        data = data[0].get('status')
    except:
        return 0
    if data:
        return data
    else:
        times = str(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
        sql = "update user  set status='%s',activationtime='%s' where email='%s'" % (1,times,email)
        SelectMysql(sql)
        return 0

# 用户提交问题
def Puts(title,content,username):
    times = str(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
    # 字符处理防止JS注入
    content = content.replace('<', '&#60;').replace('>', '&#62;').replace('\r', '<br>').replace(' ', '&nbsp;').replace('	', '&nbsp;&nbsp;&nbsp;&nbsp;').replace("'", "&#39;").replace('"', '&#34;')
    sql = "insert into question(id,title,content,fbtime,click,keywords,username) values(NULL,'%s','%s','%s',%s,'%s','%s')" % (title, content, time.strftime('%Y-%m-%d'), 1, username, username)
    SelectMysql(sql)
    sql = "SELECT * FROM question WHERE title = '%s' and username = '%s' ORDER BY id DESC LIMIT 1"%(title,username)
    data = SelectMysql(sql)
    return data

# 用户登陆
def logins(username,password):
    if validateEmail(username):
        sql = "select * from user where email='%s' and password='%s'" % (username, password)
        userdata = SelectMysql(sql)
    else:
        sql = "select * from user where username='%s' and password='%s'" %(username,password)
        userdata = SelectMysql(sql)
    if userdata:
        status = userdata[0].get('status')
        return status
    else:
        return 'error'

# 用户注册
def Regs(username,password,password1,email,ip):
    data = CheckUserData(username,password,password1,email)
    if data==1:
        if SelectMysql("select * from user where username = '%s'" % username):
            return 2
        else:
            usermd5url = pc.encrypt(email)
            ticket = pc.encrypt(username)
            RegEmail(email, username, ticket, usermd5url)

            times = str(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
            sql = "insert into user(id,username,password,email,regtime,ip) VALUES (NULL,'%s','%s','%s','%s','%s')" % (
            username, password, email, times, ip)
            SelectMysql(sql)
            return 1
    else:
        return data

# 用户HeaderTab选项设置，未调用
def HeaderTab(pagename,username):
    index = ''
    post = ''
    user = ''
    if username:
        if pagename=='index':
            index = 'active'
        if pagename=='post':
            post = 'active'
        if pagename=='user':
            user = 'active'
        data = '''
        <li class ="%s"><a href="/">首页</a></li>
        <li class ="%s"><a href ="/post">提问</a></li>
        <li class ="%s"><a href ="/user">个人中心</a></li>
         '''%(index,post,user)
        return data
    else:
        if pagename=='index':
            index = 'active'
        if pagename=='post':
            post = 'active'
        data = '''
        <li class ="%s"><a href="/">首页</a></li>
        <li class ="%s"><a href ="/post">提问</a></li>
         '''%(index,post)
        return data