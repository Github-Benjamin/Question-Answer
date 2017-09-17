# -*- coding:utf-8 -*-
# /**
#  * Created by Benjamin on 2017/9/7
#  */
import web
from model.model import *

urls = (
    '/', 'Main',
    '/login','Login',
    '/logout','Logout',
    '/user/(\d+)','User',
    '/title/(\d+)','Title',
    '/titled','Titled',
    '/huifu/(\d+)','Huifu',
    '/tubiao','Tubiao',
    '/about','About',
)

render = web.template.render("templates")

# 装饰器函数
def checklogin(func):
    def apps(*args,**kwargs):
        username = session.username
        if username:
          return  func(*args,**kwargs)
        else:
            return render.login(render.head())
    return apps

class Index(object):
    def GET(self):
        return render.login()

class Main(object):
    def GET(self):
        return render.index()

class Login(object):
    def GET(self):
        return render.login()
    def POST(self):
        return web.seeother("/")

class User(object):
    def GET(self,page):
        return render.user(userdata(page), PageNum(page, 'user', 'user'))
    def POST(self,page):
        data = web.input()
        id,username,email,status = data.get('id'),data.get('username'),data.get('email'),data.get('status')
        return render.user(screenuser(id,username,email,status), PageNum(page, 'user', 'user'))

class Title(object):
    def GET(self,page):
        return render.title(titledata(page), PageNum(page,'question','title'))
    def POST(self,page):
        data = web.input()
        id,titlename,titlecontent,title,username = data.get('id'),data.get('titlename'),data.get('titlecontent'),data.get('title'),data.get('username')
        if id and titlename and titlecontent:
           if uptitles(id,titlename,titlecontent):
               raise web.seeother('/title/%s'%page)
           else:
               return 'error'
        if id or title or username:
            return  render.title(screentitle(id,title,username), PageNum(page,'question','title'))
        else:
            return render.title(titledata(page), PageNum(page, 'question', 'title'))

class Titled(object):
    def GET(self):
        id = web.input().get('id')
        return titleds(id)

class Huifu(object):
    def GET(self,page):
        if not page:
            page = 1
        return render.huifu(huifudata(page),PageNum(page,'question_content','huifu'))
    def POST(self,page):
        data = web.input()
        id,content,title,content_user = data.get('id'),data.get('content'),data.get('title'),data.get('content_user')
        if id and content:
           if uphuifus(id,content):
               raise web.seeother('/huifu/%s'%page)
           else:
               return 'error'
        if id or title or content_user:
            return screenhuifu(id,title,content_user)
        return screenhuifu(id, title, content_user)

class Tubiao(object):
    def GET(self):
        return render.tubiao()

class About(object):
    def GET(self):
        return render.about()

class Logout(object):
    def GET(self):
        session.kill()
        raise web.seeother('/login')

def notfound():
    return web.notfound(render.login())

def internalerror():
    return web.internalerror(render.login())

if __name__ == "__main__":

    web.config.debug = False
    web.config.session_parameters['timeout'] = 10*60
    app = web.application(urls, globals())
    app.notfound = notfound
    app.internalerror = internalerror
    db = web.database(dbn='mysql', host='127.0.0.1', port=3306, user='root', pw='', db='question', charset='utf8')
    session = web.session.Session(app, web.session.DiskStore('sessions'), initializer={'username': None})
    app.run()