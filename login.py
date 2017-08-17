# -*- coding:utf-8 -*-
# /**
#  * Created by Benjamin on 2017/7/17
#  */
import web
import time
from main import RegEmail,validateEmail,CheckChina

from main import prpcrypt
pc = prpcrypt('keyskeyskeyskeys')

urls = (
    '/', 'Index',
    '/post','Post',
    '/put','Put',
    '/user','User',
    '/question/(\d+)\.html', 'Question',
    '/search','Search',
    '/login','Login',
    '/reg','Reg',
    '/activation','Activation',
    '/logout','Logout',
)

render = web.template.render("templates")

class Index(object):
    def GET(self):
        data = db.query("SELECT * FROM question ORDER BY id DESC LIMIT 10")
        username = session.username
        if username:
            return render.index(render.head(username,index='class=active'),data)
        else:
            return render.index(render.head(index='class=active'),data)

class Post(object):
    def GET(self):
        username = session.username
        if username:
            return render.put(render.head(session.username,post='class=active'))
        else:
            return render.login(render.head(post='class=active'))

class Put(object):
    def POST(self):
        username = session.username
        if username:
            data = web.input()
            title = data.get('title')
            content = data.get('content')
            print type(content)
            if (title and content):

                content=content.replace('<','&#60;').replace('>','&#62;').replace('\r','<br>').replace(' ','&nbsp;').replace('	','&nbsp;&nbsp;&nbsp;&nbsp;').replace("'","&#39;").replace('"','&#34;')

                times = str(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
                data = db.query("insert into question(id,title,content,fbtime,click,keywords,username) values(NULL,'%s','''%s''','%s',%s,'%s','%s')" % (title, content,times, 1, username,username))
                if data:
                    data = db.query("SELECT * FROM question ORDER BY id DESC LIMIT 1 ")
                    raise web.seeother('/question/%s.html' % data[0].get('id'))
                else:
                    return render.head(username,'<br><h1>服务器异常，提交问题失败</h1>')
            else:
                return render.head(username, '<br><h1>问题或描述为空，请重新输入数据</h1>')
        else:
            raise web.seeother('/')

class User(object):
    def GET(self):
        username = session.username
        if username:
            data = db.query("SELECT * FROM question where username='%s'"%str(username))
            if data:
                return render.index(render.head(username,user='class=active'), data)
            else:
                return render.head(username, '<h3>%s的用户个人中心，暂无提问数据！</h3>'%str(username),user='class=active')
        else:
            raise web.seeother('/')

class Question(object):
    def GET(self,s):
        username = session.username
        data = db.query("select * from question where id='%s'"%s)
        if not data:
            return render.head(username,'<h1>该问题不存在或已被删除</h1>')
        else:
            data = data[0]
            click = data.get('click') + 1
            db.query("update question  set click='%s' where id='%s'"%(click,s))
            data = db.query("select * from question where id='%s'" % s)
            data = data[0]
            return render.question(render.head(username),data)
    def POST(self,s):
        username = session.username
        return render.head(username,'<h1>回复功能已经关闭,请稍后再试</h1>')

class Search(object):
    def GET(self):
        username = session.username
        data = web.input()
        kw = data.get('kw')
        if kw:
            data = db.query("select * from question where title like '%s%s%s' or content like '%s%s%s'"%('%',kw,'%','%',kw,'%'))
            if data:
                return render.index(render.head(username), data)
            else:
                return render.head(username,'<h3>查无数据，请重新搜索</h3>')
        else:
            return render.head(username, '<h3>查无数据，请重新搜索</h3>')

class Login(object):
    def GET(self):
        if session.username:
            raise web.seeother('/')
        return render.login(render.head())
    def POST(self):
        data = web.input()
        username = data.get('username')
        password = data.get('password')
        if validateEmail(username):
            userdata = db.query("select * from user where email='%s' and password='%s'" % (username, password))
            try:
                userdata = userdata[0]
                status = userdata.get('status')
                username = userdata.get('username')
            except:
                status = None
        else:
            userdata = db.query("select * from user where username='%s' and password='%s'" %(username,password))
            try:
                status = userdata[0].get('status')
            except:
                status = None
        if userdata:
            if status==1:
                session.username = username
                raise web.seeother('/')
            if status==0:
                return render.head(username=None, con='<br><h1>账号未激活，请查看通过邮件激活！</h1>')
            else:
                raise web.seeother('/')
        else:
            return render.head(username=None,con='<br><h1>账号或密码错误,请重新登录！</h1>')

class Reg(object):
    def GET(self):
        return render.reg(render.head())
    def POST(self):

        data = web.input()
        username = data.get('username')
        password = data.get('password')
        password1 = data.get('password1')
        email = data.get('email')

        if (username and password and password1 and email):

            if CheckChina(username):
                return render.head(username=None, con='<h1>用户名不能包含中文字符，请重新输入</h1>')
            if password != password1:
                return render.head(username=None, con='<h1>两次密码输入不一致，请重新输入</h1>')
            if CheckChina(password):
                return render.head(username=None, con='<h1>密码不能包含中文</h1>')
            if len(username)>10:
                return render.head(username=None, con='<h1>用户名长度最大为10字符，请重新输入</h1>')
            if len(password)>16:
                return render.head(username=None, con='<h1>密码长度最长为16个字符，请重新输入</h1>')
            if not validateEmail(email):
                return render.head(username=None, con='<h1>邮件格式不合法，请重新输入</h1>')

            data = db.query("select * from user where username = '%s'" % username)
            if data:
                return render.head(username=None, con='<br><h1>用户已注册</h1>')

            ip = web.ctx.ip
            usermd5url=pc.encrypt(email)
            ticket=pc.encrypt(username)
            RegEmail(email,username,ticket,usermd5url)
            times = str(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
            db.query("insert into user(id,username,password,email,regtime,ip) VALUES (NULL,'%s','%s','%s','%s','%s')"%(username,password,email,times,ip))

            return  render.head(username=None,con='<br><h1>注册邮件已发送，请通过邮件激活账号。</h1>')

        else:
            return render.head(username=None, con='<br><h1>数据不全，请重新输入</h1>')

class Activation(object):
    def GET(self):
        web.header("Content-Type", "text/html; charset=utf-8")
        data = web.input()
        email = data.get('email')
        ticket =  data.get('ticket')

        if (email and ticket):

            # email解密
            try:
                email = pc.decrypt(email)
                ticket = pc.decrypt(ticket)
            except:
                return '非法数据'
            data = db.query("select * from user where email='%s' and username='%s'"%(email,ticket))
            if data:
                data = data[0].get('status')
                if data:
                    return render.head(username=None, con='<br><h1>账号已激活，请勿重复激活</h1>')
                else:
                    times = str(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
                    db.query("update user  set status='%s',activationtime='%s' where email='%s'" % (1,times,email))
                    return render.head(username=None, con='<br><h1>账号激活成功</h1>')
            else:
                return '账号不存在'
        else:
            return '非法数据'

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

