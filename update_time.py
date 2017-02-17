#!/usr/bin/env python
# encoding=utf-8
'''
vimwiki 中用来查找 wiki 词
'''
import fnmatch
import sys
import os
import time
from time import mktime
import re

reload(sys)
sys.setdefaultencoding('utf-8')

RESULT_FILE = 'search.md'

NOT_IN = [RESULT_FILE, 'search.wiki']


def search(path, name):
    mds = {}
    for md in os.listdir(path):
        md = os.path.basename(md)
        if os.path.isdir(path + md):  # 跳过目录
            continue
        if md in NOT_IN:  # 跳过目录特定文件名
            continue

        if(fnmatch.fnmatchcase(md.upper(), ('*%s*' % name).upper())):
            # 取文件修改时间
            modify_time = time.localtime(os.path.getmtime(path + md))
            mds[md] = modify_time
        # 按时间排序
    mds = sorted(mds.items(), key=lambda by: by[1], reverse=True)
    return mds


def update(name, time):
    pattern = re.compile(r'^\.')
    if pattern.search(name):
        return
    print name
    if name.endswith('.wiki'):
        name = name[:-len('.wiki')]
    name = '/Users/bigzhu/Dropbox/blog/data/' + name + '.md'
    time = mktime(time)
    os.utime(name, (time, time))
    print name

if __name__ == '__main__':
    for wiki in search('/Users/bigzhu/Dropbox/knowledge/data/', '*.wiki'):
        print wiki
        update(wiki[0], wiki[1])
