# /usr/bin/env python
# -*- coding: utf-8 -*-
from os.path import expanduser
import sys
home = expanduser("~")
sys.path.append(home + '/lib_p_bz')
sys.path.append('./bz_lib_p')
sys.path.append('./markdown-search')
import tornado.ioloop
import tornado.web
import time
import os
import urllib

from tornado.web import RequestHandler
import tornado_bz
import sys
from markdown_search import search

try:
    import ConfigParser
    config = ConfigParser.ConfigParser()
except ImportError:
    import configparser
    config = configparser.ConfigParser()

with open('config.ini', 'r') as cfg_file:
    config.readfp(cfg_file)
    MD_PATH = config.get('config', 'md_path')
    NOT_IN = config.get('config', 'not_in')
    AUTHOR = config.get('config', 'author')
    AUTHOR_LINK = config.get('config', 'author_link')

if NOT_IN:
    NOT_IN = NOT_IN.split(',')

MD_PATH = home + '/Dropbox/blog/'
FUCK_THE_SPIDER = []
FUCK_THE_SPIDER.append('/ganglia/index.php')
FUCK_THE_SPIDER.append('/phpmyadmin')
FUCK_THE_SPIDER.append('/hwi/')
FUCK_THE_SPIDER.append('/master-status')
FUCK_THE_SPIDER.append('/dfshealth.html')
FUCK_THE_SPIDER.append('/clusters.jsf')
FUCK_THE_SPIDER.append('/index.php')
FUCK_THE_SPIDER.append('/jobs/')
FUCK_THE_SPIDER.append('/install/index.php')
FUCK_THE_SPIDER.append('/plugins/content/s5_media_player/helper.php?fileurl=Li4vLi4vLi4vY29uZmlndXJhdGlvbi5waHA=')
FUCK_THE_SPIDER.append('/uddiexplorer/SearchPublicRegistries.jsp?operator=http://www.alibaba.com/&rdoSearch=name&txtSearchname=sdf&txtSearchkey=&txtSearchfor=&selfor=Business+location&btnSubmit=Search')
FUCK_THE_SPIDER.append('/dfshealth.jsp')
FUCK_THE_SPIDER.append('/hadoop/dfshealth.jsp')
FUCK_THE_SPIDER.append('/cogfqduzlrxy')
FUCK_THE_SPIDER.append('/jenkins/')
FUCK_THE_SPIDER.append('/zabbix/')
FUCK_THE_SPIDER.append('/solr/')
try:
    import pygments
except ImportError:
    print('you need install pygments, please run:')
    print('sudo pip install pygments')
    exit(1)
print('pygments version: ', pygments.__version__)
import markdown
try:
    from mdx_gfm import GithubFlavoredMarkdownExtension
except ImportError:
    print('you need install py-gfm, please run:')
    print('sudo pip install py-gfm')
    exit(1)
from markdown.extensions.toc import TocExtension
md = markdown.Markdown(extensions=[GithubFlavoredMarkdownExtension(), TocExtension(baselevel=3), 'markdown.extensions.toc'])
# md = markdown.Markdown(extensions=['markdown.extensions.toc'])


def removeSuffix(name):
    if name.endswith('.md'):
        return name[:-len('.md')]


def getContent(name):
    if name in NOT_IN:
        return '# 不要乱访问哦! 这不是你有权限可以看的东西!'

    name_file = open(MD_PATH + name + '.md', 'r')
    content = name_file.read()
    name_file.close()
    if 'status: draft' in content:
        return '# 这是一个机密文件, 不允许查看!'
    return content


def getModifyTime(name):
    modify_time = time.localtime(os.path.getmtime(MD_PATH + name + '.md'))
    return modify_time


def preAndOld(name):
    mds = search(MD_PATH, '*.md', NOT_IN)
    for index, item in enumerate(mds):
        # print(item[0])
        # print(name)
        if item[0] == name + '.md':
            break
    else:
        index = -1

    if len(mds) < 2 or index == -1:
        return None, None
    if index == 0:
        return None, removeSuffix(mds[index + 1][0])
    if index == len(mds):
        return removeSuffix(mds[index - 1][0]), None
    pre = removeSuffix(mds[index - 1][0])
    old = removeSuffix(mds[index + 1][0])
    del mds
    return pre, old


class blog(RequestHandler):

    '''
    显示 blog 的详细内容
    '''

    def get(self, name=None):
        import gc
        import objgraph
        # 强制进行垃圾回收
        gc.collect()
        # 打印出对象数目最多的 50 个类型信息
        objgraph.show_most_common_types(limit=5)

        # if self.request.uri in FUCK_THE_SPIDER:
        for i in FUCK_THE_SPIDER:
            if self.request.uri.startswith(i):
                self.redirect('http://zt.bdinfo.net/speedtest/wo3G.rar')
                print('!!!!fuck: ' + self.request.uri)
                return
        if name.endswith('.md'):
            name = removeSuffix(name)
            self.redirect('/' + name, permanent=True)
            return
        if name.endswith('.html'):
            name = removeSuffix(name)
            self.redirect('/' + name, permanent=True)
            return
        if name is None or name == '':
            mds = search(MD_PATH, '*.md', NOT_IN)
            name = removeSuffix(mds[0][0])
            del mds

            url_name = urllib.parse.quote(name)
            self.redirect('/' + url_name)
        else:
            content = getContent(name)

            content = md.convert(content)
            # print(md.toc)
            modify_time = getModifyTime(name)
            pre, old = preAndOld(name)

            self.render('./blog.html', title=name, content=content, time=time,
                        modify_time=modify_time, pre=pre, old=old,
                        author=AUTHOR,
                        author_link=AUTHOR_LINK,
                        toc=md.toc,
                        urllib=urllib
                        )

    def post(self):
        self.redirect('http://zt.bdinfo.net/speedtest/wo3G.rar')
        print('!!!!fuck: ' + self.request.uri)

if __name__ == "__main__":
    the_class = globals().copy()

    if len(sys.argv) == 2:
        port = int(sys.argv[1])
    else:
        port = 8888
    print(port)

    url_map = tornado_bz.getURLMap(the_class)
    url_map.append((r'/(.*)', blog))
    url_map.append((r'/static/(.*)', tornado.web.StaticFileHandler, {'path': "./static"}))

    settings = tornado_bz.getSettings()

    application = tornado.web.Application(url_map, **settings)

    application.listen(port)
    ioloop = tornado.ioloop.IOLoop().instance()
    tornado.autoreload.start(ioloop)
    ioloop.start()
