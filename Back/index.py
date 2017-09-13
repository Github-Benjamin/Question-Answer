# -*- coding:utf-8 -*-
# /**
#  * Created by Benjamin on 2017/9/7
#  */
import web

urls = (
    '/', 'Main',
    '/login','Login',
    '/logout','Logout',
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

class Logout(object):
    def GET(self):
        session.kill()
        raise web.seeother('/login')

def notfound():
    username = session.username
    return web.notfound(web.seeother('/login'))

def internalerror():
    username = session.username
    return web.internalerror(web.seeother('/login'))

if __name__ == "__main__":

    web.config.debug = False
    web.config.session_parameters['timeout'] = 10*60
    app = web.application(urls, globals())
    app.notfound = notfound
    app.internalerror = internalerror
    db = web.database(dbn='mysql', host='127.0.0.1', port=3306, user='root', pw='', db='question', charset='utf8')
    session = web.session.Session(app, web.session.DiskStore('sessions'), initializer={'username': None})
    app.run()