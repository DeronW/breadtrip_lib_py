#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
import json
from django.conf import settings


class SegTxt(object):
    """
    结巴分词客户端
    ===============
    method 只有三种模式: search, full, default
    search:  搜索模式
    full: 全模式
    default: 精确模式, 当method不为search or full时默为default
    """

    def __init__(self):
        self.HOST = settings.TCPSERVER_HOST
        self.PORT = 8888

    def cut(self, txt, method=None):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.HOST, self.PORT))
        if method:
            value = "%s|%s&&" % (method, txt)
        else:
            value = "%s|%s&&" % ("default", txt)
        try:
            self.sock.send(value)
            self.sock.settimeout(5)
            data = self.sock.recv(1024)
            data = json.loads(data)
        except:
            data = []
        self.sock.close()
        return data


