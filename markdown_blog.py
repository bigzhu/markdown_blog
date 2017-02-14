#!/usr/bin/env python
# -*- coding: utf-8 -*-
from os.path import expanduser
import sys
home = expanduser("~")
sys.path.append(home + '/lib_p_bz')
sys.path.append('./markdown-search')
import tornado.ioloop
import tornado.web
import public_bz

from tornado.web import RequestHandler
import tornado_bz
import sys
from markdown_search import search

MD_PATH = home + '/Dropbox/blog/data/'

import houdini as h
import misaka as m
from pygments import highlight
from pygments.formatters import HtmlFormatter, ClassNotFound
from pygments.lexers import get_lexer_by_name

NOT_IN = ['mac app id passwd']


def removeSuffix(name):
    if name.endswith('.md'):
        return name[:-len('.md')]


class HighlighterRenderer(m.HtmlRenderer):

    def blockcode(self, text, lang):
        try:
            lexer = get_lexer_by_name(lang, stripall=True)
        except ClassNotFound:
            lexer = None

        if lexer:
            formatter = HtmlFormatter()
            return highlight(text, lexer, formatter)
        # default
        return '\n<pre><code>{}</code></pre>\n'.format(
            h.escape_html(text.strip()))

renderer = HighlighterRenderer()
md = m.Markdown(renderer, extensions=('fenced-code',))


def gfm(str_md=''):
    '''
    transform the markdown text to html, using github favoured markdown
    usage: str_html = gfm(str_md)
    '''
    return md(str_md)
    # str_html = misaka.html(str_md,
    #                        extensions=misaka.EXT_NO_INTRA_EMPHASIS | misaka.EXT_FENCED_CODE |
    #                        misaka.EXT_AUTOLINK | misaka.HTML_HARD_WRAP |
    #                        misaka.EXT_TABLES | misaka.HTML_USE_XHTML |
    #                        misaka.HTML_HARD_WRAP)
    # return str_html


def getContent(name):
    if name in NOT_IN:
        return '# 不要乱访问哦! 这不是你有权限可以看的东西!'
    try:
        name_file = open(MD_PATH + name + '.md', 'r')
        content = name_file.read()
        name_file.close()
        return content
    except IOError:
        print public_bz.getExpInfoAll()
        return '0'


class blog(RequestHandler):

    '''
    显示 blog 的详细内容
    '''

    def get(self, name=None):
        if name is None or name == '':
            mds = search(MD_PATH, '*', NOT_IN)
            name = removeSuffix(mds[0][0])
            self.redirect('/' + name)
        else:
            print name
            content = getContent(name)
            content = gfm(content)

            self.render('./blog.html', title=name, content=content)


if __name__ == "__main__":
    the_class = globals().copy()

    if len(sys.argv) == 2:
        port = int(sys.argv[1])
    else:
        port = 8888
    print port

    url_map = tornado_bz.getURLMap(the_class)
    url_map.append((r'/(.*)', blog))
    url_map.append((r'/static/(.*)', tornado.web.StaticFileHandler, {'path': "./static"}))

    settings = tornado_bz.getSettings()

    application = tornado.web.Application(url_map, **settings)

    application.listen(port)
    ioloop = tornado.ioloop.IOLoop().instance()
    tornado.autoreload.start(ioloop)
    ioloop.start()
