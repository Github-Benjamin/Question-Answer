#!/usr/bin/env python
# coding: utf-8
import web,time

urls = (
	'/','Index',
	'/reg','Reg',
	'/post','Post',
	'/login','Login',
	'/logout','Logout',
	'/user','User',
	'/question/(\d+)\.html','Question',
	'/put','Put',
)

render = web.template.render("templates")

allowed = (
	('admin','123123'),
)

web.config.debug = False
app = web.application(urls, locals())
session = web.session.Session(app, web.session.DiskStore('sessions'))
db = web.database(dbn='mysql',host='127.0.0.1',port=3306,user='root',pw='',db='question',charset='utf8')

class Put:
	def POST(self):
		if not session.get('logged_in', False):
			raise web.seeother('/login')
		i = web.input()
		title = i.get('title')
		content = i.get('content')
		if not title and not content:
			return render.head('<h1>问题和描述都不能为空</h1>')
		data = db.query("insert into question(id,title,content,fbtime,click,keywords) values(NULL,'%s','%s','%s',%s,'%s')" %(title,content,time.strftime('%Y-%m-%d'),20,u'关键词'))
		if not data:
			return render.head('<h1>服务器出现问题,该问题提交失败</h1>')
		data = db.query("SELECT * FROM question ORDER BY id DESC LIMIT 1 ")
		raise web.seeother('/question/%s.html' %data[0].get('id'))

class Question:
	def GET(self,s):
		data = db.query("select * from question where id=%s" %s)
		if not data:
			return render.head('<h1>该问题不存在或已被删除</h1>')
		else:
			return render.question(render.head(),data[0])
	def POST(self,s):
		return render.head('<h1>回复功能已经关闭,请稍后再试</h1>')

class User:
	def GET(self):
		data = db.query("select * from question order by rand() limit 2")
		return render.index(render.head(),data)

class Reg:
	def GET(self):
		return render.reg.html(render.head())
	def POST(self):
		return

class Index:
	def GET(self):
		#if session.get('logged_in',False):
		data = db.query("SELECT * FROM question ORDER BY id DESC LIMIT 10")
		return render.index(render.head(),data)
		#raise web.seeother('/login')

class Login:
	def GET(self):
		if session.get('logged_in',False):
			raise web.seeother('/')
		return render.login(render.head())
	def POST(self):
		i = web.input()
		username = i.get('username')
		passwd = i.get('passwd')
		us = db.query("select * from user where username='%s' and passwd='%s'" %(username,passwd))
		if us:
			session.logged_in = True
			#web.setcookie('system_mangement', '', 60)
			raise web.seeother('/')
		else:
			return render.head('<br><h1>账号或密码错误,请重新登录</h1>')

class Logout:
	def GET(self):
		session.logged_in = False
		raise web.seeother("/login")

class Post:
	def GET(self):
		if session.get('logged_in',False):
			return render.put(render.head())
		raise web.seeother('/login')

if __name__ == '__main__':
	app.run()
