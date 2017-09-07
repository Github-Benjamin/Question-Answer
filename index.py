# -*- coding:utf-8 -*-
# /**
#  * Created by Benjamin on 2017/9/7
#  */
import time
import web
from model.plugins import *
from model.model import *

urls = (
    '/', 'Index',
    '/page/(\d+)','Page',
    '/post','Post',
    '/put','Put',
    '/user','User',
    '/question/(\d+)', 'Question',
    '/search','Search',
    '/login','Login',
    '/reg','Reg',
    '/activation','Activation',
    '/logout','Logout',
)

render = web.template.render("templates")

class Index(object):
    def GET(self):
        username = session.username
        if username:
            return render.index(render.head(username),PageData(1),PageNum(1))
        else:
            return render.index(render.head(),PageData(1),PageNum(1))

class Page(object):
    def GET(self,page):
        username = session.username
        if username:
            return render.index(render.head(username),PageData(page),PageNum(page))
        else:
            return render.index(render.head(),PageData(page),PageNum(page))

class Post(object):
    def GET(self):
        username = session.username
        if username:
            return render.put(render.head(session.username))
        else:
            return render.login(render.head())

class Put(object):
    def POST(self):
        username = session.username
        if username:
            data = web.input()
            title = data.get('title')
            content = data.get('content')
            if (title and content):
                data = Puts(title,content,username)
                if data:
                    raise web.seeother('/question/%s' % data[0].get('id'))
                else:
                    return render.public(render.head(username), '<h3>服务器异常，提交问题失败</h3>')
            else:
                return render.public(render.head(username), '<h3>问题或描述为空，请重新输入数据</h3>')
        else:
            raise web.seeother('/')

class User(object):
    def GET(self):
        username = session.username
        if username:
            data = db.query("SELECT * FROM question where username='%s'"%str(username))
            if data:
                return render.index(render.head(username), data)
            else:
                return render.public(render.head(username),'<h3>%s的用户个人中心，暂无提问数据！</h3>'%str(username))
        else:
            raise web.seeother('/')

class Question(object):
    def GET(self,s):
        username = session.username
        data = db.query("select * from question where id='%s'"%s)
        if not data:
            return render.public(render.head(username), '<h3>该问题不存在或已被删除</h3>')
        else:
            data = data[0]
            click = data.get('click') + 1
            db.query("update question  set click='%s' where id='%s'"%(click,s))
            data = db.query("select * from question where id='%s'" % s)
            data = data[0]
            return render.question(render.head(username),data)
    def POST(self,s):
        username = session.username
        return render.public(render.head(username), '<h3>回复功能已经关闭,请稍后再试</h3>')

class Search(object):
    def GET(self):
        username = session.username
        kw = web.input().get('kw')
        if kw:
            data = Searchs(kw)
            if data:
                return render.index(render.head(username),data)
            else:
                return render.public(render.head(username),'<h3>查无数据，请重新搜索</h3>')
        else:
            return render.public(render.head(username), '<h3>查无数据，请重新搜索</h3>')

class Login(object):
    def GET(self):
        if session.username:
            raise web.seeother('/')
        return render.login(render.head())
    def POST(self):
        data = web.input()
        username = data.get('username')
        password = data.get('password')
        status = logins(username,password)
        if status==1:
            session.username = username
            raise web.seeother('/')
        if status==0:
            return render.public(render.head(), '<h3>账号未激活，请查看邮件并激活！</h3>')
        if status=='error':
            return render.public(render.head(), '<h3>账号或密码错误,请重新登录！</h3>')
        else:
            raise web.seeother('/')

class Reg(object):
    def GET(self):
        return render.reg(render.head())
    def POST(self):
        data = web.input()
        username,password,password1,email = data.get('username'),data.get('password'),data.get('password1'),data.get('email')
        ip = web.ctx.ip
        data = Regs(username,password,password1,email,ip)
        if data==2:
            return render.public(render.head(), '<h3>该用户名已注册，请勿重复注册！</h3>')
        if data==1:
            return render.public(render.head(), '<h3>注册邮件已发送，请通过邮件激活账号。</h3>')
        else:
            return render.public(render.head(), data)

class Activation(object):
    def GET(self):
        web.header("Content-Type", "text/html; charset=utf-8")
        data = web.input()
        email = data.get('email')
        ticket =  data.get('ticket')
        if (email and ticket):
            # email解密
            try:
                email,ticket = pc.decrypt(email),pc.decrypt(ticket)
            except:
                return render.public(render.head(),'<h3>非法数据</h3>')
        if Activations(email,ticket):
            return render.public(render.head(),'<h3>账号已激活，请勿重复激活</h3>')
        else:
            return render.public(render.head(), '<h3>账号激活成功</h3>')

class Logout(object):
    def GET(self):
        session.kill()
        raise web.seeother('/')

def notfound():
    username = session.username
    return web.notfound(render.head(username,render.error()))

def internalerror():
    username = session.username
    return web.internalerror(render.head(username,render.error()))

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
# db = web.database(dbn='mysql', host='127.0.0.1', port=3306, user='root', pw='', db='question', charset='utf8')
# session = web.session.Session(app, web.session.DiskStore('sessions'), initializer={'username': None})
# app = app.wsgifunc()