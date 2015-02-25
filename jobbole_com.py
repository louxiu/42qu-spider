#coding:utf-8
from spider.spider import route, Handler, spider, extract
import _env
from os.path import abspath, dirname, join
from operator import itemgetter
from html2txt import html2txt

@route("/page/(\d+)/")
class _(Handler):
    def get(self,page):
        for html in self.extract_all('<h2><a  target="_blank" href="http://blog.jobbole.com', '<!-- .entry-content -->'):
            id = html[:html.find('"')] 
            title = extract('/','<',html).split(">",1)[-1]
            link_html = extract('<div class="entry-content">','</p>', html)
            link_html = extract('<p', None, link_html)
            txt = html2txt(link_html)
            if "http://" in txt:
                print "http://blog.jobbole.com%s"%id
                print title
                print txt  
                print ""

if __name__ == '__main__':
    for i in xrange(1,159):
        spider.put('http://blog.jobbole.com/page/%s/'%i)

    #10个并发抓取线程 , 网页读取超时时间为30秒
    spider.run(10, 30)

