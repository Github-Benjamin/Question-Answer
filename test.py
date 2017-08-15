# coding: utf-8
import web

db = web.database(dbn='mysql',host='127.0.0.1',port=3306,user='root',pw='',db='question',charset='utf8')
data = db.query("select * from user where username='%s'"%'Benjamin')

if data:
    print 'yes'
else:
    print 'no'