#coding:utf-8
from spider.spider import route, Handler, spider
import _env
from os.path import abspath, dirname, join
from operator import itemgetter

PREFIX = join(dirname(abspath(__file__)))

@route('/snap/(\d+)')
class portal(Handler):
    def get(self, id):
        link = self.extract('源地址：<a href="','"')
        #name = self.extract('作者：','&nbsp;&nbsp;|&nbsp;&nbsp;')
        title = self.extract('<h1 style="margin-bottom:0;">','</h1>')
        if link:
            print id, link,  title.replace("\n"," ")

if __name__ == '__main__':

    URL = "http://ucdchina.com/snap/%s"
    for i in xrange(1250,12460+1):
        spider.put(URL%i)

    #10个并发抓取线程 , 网页读取超时时间为30秒
    spider.run(10, 30)

