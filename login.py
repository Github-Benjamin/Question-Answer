# -*- coding:utf-8 -*-
# /**
#  * Created by Benjamin on 2017/7/17
#  */
import web
from main import notfound,internalerror

urls = (
    '/', 'Index',
    '/post','Post',
    '/user','User',
    '/question/(\d+)\.html', 'Question',
    '/login','Login',
    '/reg','Reg',
    '/logout','Logout',
)

render = web.template.render("templates")

class Index(object):
    def GET(self):
        data = db.query("SELECT * FROM question ORDER BY id DESC LIMIT 10")
        username = session.username
        if username:
            return render.index(render.head(username),data)
        else:
            return render.index(render.head(),data)

class Post(object):
    def GET(self):
        username = session.username
        if username:
            return render.put(render.head(session.username))
        else:
            return render.reg(render.head())

class User(object):
    def GET(self):
        return render.head(session.username,'<h1>用户个人中心</h1>')

class Question:
	def GET(self,s):
		data = db.query("select * from question where id=%s" %s)
		if not data:
			return render.head(None,'<h1>该问题不存在或已被删除</h1>')
		else:
			return render.question(render.head(),data[0])
	def POST(self,s):
		return render.head(None,'<h1>回复功能已经关闭,请稍后再试</h1>')

class Login(object):
    def GET(self):
        if session.username:
            raise web.seeother('/')
        return render.login(render.head())
    def POST(self):
        data = web.input()
        username = data.get('username')
        password = data.get('password')
        userdata = db.query("select * from user where username='%s' and password='%s'" %(username,password))
        print userdata
        if userdata:
            print 1111
            session.username = username
            raise web.seeother('/')
        else:
            return render.head(username=None,con='<br><h1>账号或密码错误,请重新登录</h1>')

class Reg(object):
    def GET(self):
        return render.reg(render.head())
    def POST(self):
        data = web.input()
        username = data.get('username')
        password = data.get('password')
        password1 = data.get('password1')
        tel = data.get('tel')
        if (username and password and password1 and tel):
            if password != password1:
                return render.head(username=None, con='<h1>两次密码输入不一致，请重新输入</h1>')
            data = db.query("select * from user where username = %s" % username)
            if data:
                return render.head(username=None, con='<br><h1>用户已注册</h1>')
            db.query("insert into user(id,username,password,tel) VALUES (NULL,%s,%s,%s)"%(username,password,tel))
            session.user = username
            username = session.user
            return render.head(username,'<br><h1>注册成功</h1>')
        else:
            return render.head(username=None, con='<br><h1>数据不全，请重新输入</h1>')


class Logout(object):
    def GET(self):
        session.kill()
        raise web.seeother('/')



if __name__ == "__main__":

    web.config.debug = False
    web.config.session_parameters['timeout'] = 10*60

    app = web.application(urls, globals())

    app.notfound = notfound
    app.internalerror = internalerror

    db = web.database(dbn='mysql', host='127.0.0.1', port=3306, user='root', pw='', db='question', charset='utf8')
    session = web.session.Session(app, web.session.DiskStore('sessions'), initializer={'username': None})

    app.run()

# web.config.debug = False
# web.config.session_parameters['timeout'] = 10*60
# app = web.application(urls, globals())
# app.notfound = notfound
# app.internalerror = internalerror
# session = web.session.Session(app, web.session.DiskStore('sessions'), initializer={'user': None,'admin':None})
# app = app.wsgifunc()