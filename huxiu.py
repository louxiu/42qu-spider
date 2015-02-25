# coding:utf-8
from spider.spider import route, Handler, spider

HTTP = 'http://www.huxiu.com%s'
TAG_ARTICLE_DICT = {}


@route('/tagslist/all\.html')
class Tags(Handler):
    def get(self):
        for link in self.extract_all('<li class="js-tag-w"><a href="', '</a>'):
            # filtering hot tags which have target label
            if link.find('target') == -1:
                sp_result = link.split('">')

                if len(sp_result) != 2:
                    continue
                link_href = sp_result[0]
                link_name = sp_result[1]

                # Lazy... Just using url as key, tag id should be used.
                tag_url = HTTP % link_href
                TAG_ARTICLE_DICT[tag_url] = {'tag_name': link_name,
                                             'article_list': []}
                spider.put(tag_url)


@route('/tags/\d+\.html')
class Articles(Handler):
    def get(self):
        for link in self.extract_all('<h3><a href="', '</a>'):
            article_result = link.split('">')

            if len(article_result) != 2:
                continue
            article_name = article_result[1]
            tag_url = self.get_tag_url()
            # tag_url must be in TAG_ARTICLE_DICT
            TAG_ARTICLE_DICT[tag_url]['article_list'].append(article_name)

    def get_tag_url(self):
        url = self.request.url
        return url


def print_result():
    for value in TAG_ARTICLE_DICT.values():
        print value['tag_name']
        for idx, article_name in enumerate(value['article_list']):
            print ' ', idx+1, '.', article_name


if __name__ == '__main__':
    spider.put('http://www.huxiu.com/tagslist/all.html')
    # 10个并发抓取线程 , 网页读取超时时间为30秒
    spider.run(10, 30)
    print_result()
