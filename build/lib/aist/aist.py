# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import requests, json
from download import Download
from msg import Msg

if __name__ == '__main__':

    # down = Download('PC8805191')
    # down = Download('PC3972989')
    # down.all('d:/test/')
    # down.ls('1.txt')

    msg = Msg('MS1836445')
    msg.push('')
    msg.put('效果很吼')

