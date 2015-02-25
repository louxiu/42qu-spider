#coding:utf-8
from spider.spider import route, Handler, spider
import _env
from os.path import abspath, dirname, join
from operator import itemgetter
import json
from yajl import dumps
from html2txt import html2txt

PREFIX = join(dirname(abspath(__file__)))

def print_i(i, title_list=[]):
    api_url = i.get('api_url', '')
    if api_url and 'app_id' in api_url:
        print api_url
        print ">>" , ' > '.join(title_list), '>', i['title'] , i.get('pk', '')  
        print i.get('pic', '')
        print i.get('list_icon', '')
        print i.get('list_title', '')
        #spider.put(api_url)


    for j in (i.get('sons', '') or ()):
        print_i(j, title_list+[i['title']])


@route('(.*)')
class _(Handler):
    def get(self, path):
        data = json.loads(self.html)
        if path == '/zaker/apps.php':
            data = data['data']['datas']
            for i in data:
                print_i(i)
        else:
            if data['msg'] != 'ok':return
            data = data['data']
            if 'articles' in data:
                for txt in data['articles']:
                    if 'full_url' in txt:
                        url = txt['full_url']
                        #spider.put( url)
                        #print url 
            else:
                print html2txt(data['content'])


#http://iphone.myzaker.com/l.php?l=50b7f4a1497959972f00007e
#a.myzaker.com/aa/201210/677/508f73234979593b55000023.htm?
#@route('/(.*)\.htm')
#class _(Handler):
#    def get(self, path):
#        print path 


if __name__ == '__main__':
    spider.put('http://iphone.myzaker.com/zaker/apps.php?act=getAllAppsData')
    #10个并发抓取线程 , 网页读取超时时间为30秒
    spider.run(10, 30)

