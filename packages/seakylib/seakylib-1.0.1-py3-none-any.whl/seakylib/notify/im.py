#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Seaky
# @Date:   2019/8/14 11:50

import hashlib
import time
from functools import partial

import requests


def im(content, url, auth, mode, to, add_time=False, log=None):
    '''
    :param s:
    :param url:
    :param auth:
    :param mode:
    :param to:
    :param add_time:    服务端自动添加时间
    :param log:
    :return:
    '''
    if mode == 'popo' and '@' not in to:
        to += '@corp.netease.com'
    payload = {'timestamp': int(time.time()),
               'mode': mode,
               'auth': auth,
               'to': to,
               'content': content,
               'add_time': add_time,
               }
    payload['sign'] = hashlib.md5('{timestamp}{mode}{auth}{to}{content}'.format(**payload).encode('utf-8')).hexdigest()
    if log:
        log.info('{}'.format(content))
    return requests.post(url, payload)


popo = partial(im, mode='popo')
yx = partial(im, mode='yx')
sms163 = partial(im, mode='sms163')
sms = partial(im, mode='sms')
