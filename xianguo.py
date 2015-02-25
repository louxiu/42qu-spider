#coding:utf-8
from spider.spider import route, Handler, spider, extract
import _env
from json import dumps
from os.path import abspath, dirname, join
from operator import itemgetter
from html2txt import html2txt, unescape

@route('/(\d+)')
class _(Handler):
    def get(self, id):
        title = self.extract('<div class="beings-name">','</div>')
        if not title:
            return
        title = unescape(title)
        link =  self.extract('<div class="beings-website"><a href="','"')
        if not link:
            return
        txt = self.extract('<div class="beings-description">','</div>')
        if txt:
            txt = unescape(txt)
        img = extract(
            'src="',
            '"', 
            self.extract('<a class="avatar" href="/','</a>')
        )
        print dumps([id, img, link,  title, txt or ''])


@route('/find/recommend')
class _(Handler):
    def get(self):
        now_id = int(self.get_argument("id", 0))
        page = int(self.get_argument("pi", 0))
        if now_id:
            for link in self.extract_all('<h3 class="nickname">','</h3>'):
                link = extract('"/','"', link)
                spider.put("http://xianguo.com/"+link)
            if page == 0:
                page_list = set(self.extract_all("href=\"/find/recommend?pi=","&"))
                for i in map(int,page_list):
                    if page:
                        spider.put("http://xianguo.com/find/recommend?id=%s&pi=%s"%(now_id,page))
        else:
            for id in self.extract_all(
                'href="/find/recommend?id=', '"'
            ):
                spider.put("http://xianguo.com/find/recommend?id=%s&pi=0"%id)

if __name__ == '__main__':

    URL = 'http://xianguo.com/find/recommend'
    spider.put(URL)

    #10个并发抓取线程 , 网页读取超时时间为30秒
    spider.run(10, 30)

