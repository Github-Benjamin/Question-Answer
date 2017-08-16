# -*- coding:utf-8 -*-
# /**
#  * Created by Benjamin on 2017/7/17
#  */
import re
from smtplib import SMTP_SSL
from email.header import Header
from email.mime.text import MIMEText
from Crypto.Cipher import AES
from binascii import b2a_hex, a2b_hex

import sys
reload(sys)
sys.setdefaultencoding('utf8')

class prpcrypt():
    def __init__(self, key):
        self.key = key
        self.mode = AES.MODE_CBC

    # 加密函数，如果text不是16的倍数【加密文本text必须为16的倍数！】，那就补足为16的倍数
    def encrypt(self, text):
        cryptor = AES.new(self.key, self.mode, self.key)
        # 这里密钥key 长度必须为16（AES-128）、24（AES-192）、或32（AES-256）Bytes 长度.目前AES-128足够用
        length = 16
        count = len(text)
        add = length - (count % length)
        text = text + ('\0' * add)
        self.ciphertext = cryptor.encrypt(text)
        # 因为AES加密时候得到的字符串不一定是ascii字符集的，输出到终端或者保存时候可能存在问题
        # 所以这里统一把加密后的字符串转化为16进制字符串
        return b2a_hex(self.ciphertext)

    # 解密后，去掉补足的空格用strip() 去掉
    def decrypt(self, text):
        cryptor = AES.new(self.key, self.mode, self.key)
        plain_text = cryptor.decrypt(a2b_hex(text))
        return plain_text.rstrip('\0')

def RegEmail(useremail,usermd5url):
    mail_info = {
        "hostname": "smtp.qq.com",
        "username": "benjamin_v@qq.com",
        "password": "tavplxghnxxxxxxxx",
        "from": "benjamin_v@qq.com",
        "to": "%s"%useremail,
        "mail_subject": "WelCome to Python Question&Answer",
        "mail_text": '''<html>
    <head><meta charset="UTF-8"></head>
    <body>
        <br>
        <h3>&#8195;WelCome to Python Question&Answer</h3>
        <br><br>
        <p>&#8195;&#8195;&#8195;感谢您注册Python问答系统，Activate Link：<a href="http://127.0.0.1:8080/activation?email=%s&ticket=Benjamin" style="text-decoration:none">点击激活账号</a></p>
        <p>&#8195;&#8195;&#8195;Click Activate Link：<a href="http://127.0.0.1:8080/activation?email=%s&ticket=Benjamin" style="text-decoration:none">http://127.0.0.1:8080/activation?email=%s&ticket=Benjamin</a></p>
        <br><img>&#8195;&#8195;&#8195;如果以上链接无法点击，请联系开发者企鹅：<a href="tencent://message/?uin=350105629&Site=&Menu-=yes" style="text-decoration:none"><img src="http://www.wzsky.net/img2015/uploadimg/20150303/1022549.png" style="height: 42px;vertical-align:middle" alt="icon">350105629</a></p>
        &#8195;&#8195;&#8195;----------------------------
        <br><br>
        &#8195;&#8195;&#8195;<img src="http://v1.qzone.cc/avatar/201507/15/18/33/55a636e158719534.jpg!200x200.jpg" alt="350105629" style="vertical-align:middle;height: 60px"> Author： Benjamin</p>
    </body>
</html>'''%(usermd5url,usermd5url,usermd5url),
    }

    smtp = SMTP_SSL(mail_info["hostname"])
    smtp.set_debuglevel(1)
    smtp.ehlo(mail_info["hostname"])
    smtp.login(mail_info["username"], mail_info["password"])

    msg = MIMEText(mail_info["mail_text"], "html","utf-8")
    msg["Subject"] = Header(mail_info["mail_subject"],"utf-8")
    msg["from"] = mail_info["from"]
    msg["to"] = mail_info["to"]
    try:
        smtp.sendmail(mail_info["from"], mail_info["to"], msg.as_string())
    except:
        pass

def validateEmail(email):
    if len(email) > 7:
        if re.match("^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$", email) != None:
            return 1
        else:
            return 0

def CheckChina(user):
    zhPattern = re.compile(u'[\u4e00-\u9fa5]+')
    user = u'%s'%user
    match = zhPattern.search(user)
    return match
