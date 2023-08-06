#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Seaky
# @Date:   2019/8/12 10:46

import os
import re
import shutil
import socket
import traceback
from pathlib import Path

import psutil

TERM_WIDTH, TERM_DEPTH = shutil.get_terminal_size((80, 20))
LIB_DIR = 'seakylib'


def get_hostname():
    return socket.gethostname()


def get_if(name=None):
    d = psutil.net_if_addrs()
    if name:
        return {k: v for k, v in d.items() if k.startswith(name)}
    return d


def get_pwd():
    '''
    即使被上层调用，也会返回lib所在目录
    '''
    r = Path(os.path.split(os.path.realpath(__file__))[0])
    parts = r._parts
    return os.path.join(*parts[:parts.index(LIB_DIR)])


def get_caller(top=True):
    '''返回用户调用函数，过滤lib'''
    es = traceback.extract_stack()
    l = es if top else es[::-1]
    for x in l:
        if not re.search('({}|pydev)'.format(LIB_DIR), x.filename):
            return Path(x.filename)
