# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from download import AistBase


class Msg(AistBase):
    def __init__(self, key):
        self.key = key

    def push(self, msg):
        self.api('msg', {'key': self.key, 'method': 'push', 'msg': msg})

    def put(self, msg):
        self.api('msg', {'key': self.key, 'method': 'put', 'msg': msg})
