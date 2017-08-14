# /**
#  * Created by Benjamin on 2017/7/17
#  */
import web

def notfound():
    return web.notfound("Sorry, the page you were looking for was not found.")

def internalerror():
    return web.internalerror("Bad, bad server. No donut for you.")