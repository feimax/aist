# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import requests, json


class AistBase:
    def __init__(self):
        pass

    @staticmethod
    def api(api_name, data):
        uri = 'http://sd.treee.com.cn/%s' % api_name
        response = requests.post(uri, data=data)
        print(response.text)
        return json.loads(response.text)


class Msg(AistBase):
    def __init__(self, key):
        self.key = key

    def push(self, msg):
        self.api('msg', {'key': self.key, 'method': 'push', 'msg': msg})

    def put(self, msg):
        self.api('msg', {'key': self.key, 'method': 'put', 'msg': msg})
