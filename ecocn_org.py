#coding:utf-8
from spider.spider import route, Handler, spider
import _env
from os.path import abspath, dirname, join
from operator import itemgetter

PREFIX = join(dirname(abspath(__file__)))
HTTP = 'http://www.ecocn.org/%s'

@route('/portal\.php')
class portal(Handler):
    def get(self):
        for link in self.extract_all('<dt class="xs2"><a href="', '"'):
            spider.put(HTTP%link)


@route('/article-\d+-\d+.html')
class article(Handler):
    def get(self):
        link = self.extract( 'class="pn" href="', '" target=""> 中英对照')
        spider.put(HTTP%link)



@route('/forum\.php')
class forum(Handler):
    from mako.lookup import Template
    template = Template(filename=join(PREFIX, 'template/rss.xml'))

    page = []

    def get(self):
        name = self.extract('id="thread_subject">', '</a>')
        if not name:
            return
        name = name.split(']', 1)[-1].strip()
        html = self.extract('<div class="t_fsz">', '<div id="comment_')
        html = html[:html.rfind('</div>')]
        tid = int(self.get_argument('tid'))
        print tid, name
        self.page.append((tid, self.request.url, name, html))

    @classmethod
    def write(cls):
        page = cls.page
        page.sort(key=itemgetter(0), reverse=True)
        with open(join(PREFIX, 'ecocn_org.xml'), 'w') as rss:
            rss.write(
                cls.template.render(
                    rss_title='经济学人 . 中文网',
                    rss_link='http://www.ecocn.org',
                    li=[
                        dict(
                            link=link,
                            title=title,
                            txt=txt
                        ) for id, link, title, txt in cls.page
                    ]
                )
            )

if __name__ == '__main__':
    spider.put('http://www.ecocn.org/portal.php?mod=list&catid=1')
    #10个并发抓取线程 , 网页读取超时时间为30秒
    spider.run(10, 30)

