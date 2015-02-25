# coding:utf-8
from spider.spider import route, Handler, spider
import re
import commands
import os

# http://dark7110.blog.fc2.com/blog-entry-24.html

HTTP = 'http://www.blgl8.com/%s'
VOLUMES_NAME_DICT = {}


@route('/comic-i/blgl\d+/')
class Volumes(Handler):
    re_link_and_name = re.compile('^.*(http://.*)\'>(.*)')

    def get(self):
        for link in self.extract_all('<div><a title=', '</a>'):
            linke_name_res = self.re_link_and_name.match(link)
            if linke_name_res:
                volume_link = linke_name_res.group(1)
                volume_name = linke_name_res.group(2)
                print volume_link, volume_name
                VOLUMES_NAME_DICT[volume_link] = volume_name
                if not os.path.exists(volume_name):
                    os.mkdir(volume_name)
                spider.put(volume_link)
                break
            else:
                pass


@route('/manhua-v/\d+cv\d+/')
class Volume(Handler):
    def get_array_files(self, s_files):
        # print s_files
        status, output = commands.getstatusoutput("node unsuan.js " + s_files)
        if status == 0:
            array_files = output.split('|')
            return array_files

    def get_volume_name(self):
        volume_name = VOLUMES_NAME_DICT[self.request.url]
        return volume_name

    def get(self):
        for segment in self.extract_all('<script>var s_files=\"', '</script>'):
            segment_list = segment.split('";')
            s_files = segment_list[0]
            # http://www.blgl8.com/script/ds/ds.js
            s_ds = 'http://comic.1mh.in:2813/'
            s_path = segment_list[1].split('="')[1]
            array_files = self.get_array_files(s_files)
            volume_name = self.get_volume_name()

            for pic_file in array_files:
                # print volume_name + s_ds + s_path + pic_file
                wget_command = 'wget ' + s_ds + s_path + pic_file + \
                               " -P " + volume_name
                print wget_command
                # status, output = commands.getstatusoutput(wget_command)
                # print status, output

if __name__ == '__main__':
    # spider.put('http://www.blgl8.com/comic-i/blgl44469/')
    spider.put('http://www.blgl8.com/comic-i/blgl39895/')
    spider.run(1, 5)
