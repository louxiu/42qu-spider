#coding:utf-8

import re
from urlparse import urlparse


class Route(object):
    def __init__(self):
        self.map = []

    def match(self, url):
        for r, f in self.map:
            m = r.match(url)
            if m:
                return f, m.groups()
        #print 'WARNING :', url, 'not match any hanlder'
        return None, None

    def __call__(self, path):
        if not path.endswith('$'):
            path += '$'
        re_path = re.compile(path)
        def _(func):
            self.map.append((re_path, func))
            return func
        return _

route = Route()

class Host(object):
    def __init__(self):
        self._host = {}

    def __call__(self, host, path=".*"):
        _host = self._host
        if host not in _host:
            _host[host] = Route() 
        return _host[host](path)

    def match(self, host, path):
        _host = self._host
        func = None 
        if host in _host:
            func = _host[host].match(path)[0]

        return func
       
    def match_by_url(self, url):
        o = urlparse(url)
        return self.match(o.netloc,o.path) 

host = Host()

if __name__ == "__main__":
    #from route import host
    @host("baidu.com")
    def extract(html):
        return html+" test"

    url = "http://baidu.com/xxxx/xxx"
    html = "hi"

    func = host.match_by_url(url)
    if func:
        html = func(html)
    
    print html
    
    


