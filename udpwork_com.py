#coding:utf-8
from spider.spider import route, Handler, spider
import _env
from os.path import abspath, dirname, join
from operator import itemgetter

PREFIX = join(dirname(abspath(__file__)))

@route('/site/(\d+).html')
class portal(Handler):
    def get(self, id):
        h2 = self.extract('<h2>','</h2>')
        link = self.extract('<p>链接: <a href="','"')
        h3 = self.extract('<h3>日志列表(',')</h3>')

        if h2:
            print h3, link, h2

if __name__ == '__main__':

    URL = "http://www.udpwork.com/site/%s.html"
    for i in xrange(2,240):
        spider.put(URL%i)

    #10个并发抓取线程 , 网页读取超时时间为30秒
    spider.run(10, 30)

