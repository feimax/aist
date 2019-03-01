# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
from os.path import join
import qiniu
import requests, json
from tqdm import tqdm
from qiniu import etag
import multiprocessing
from multiprocessing.pool import ThreadPool as Pool
from multiprocessing import cpu_count
import time


def get_image_pool(img_args):
    image_url = img_args['image_url']
    image_code = img_args['image_code']
    pbar = img_args['pbar']

    img = requests.get(image_url)
    with open(image_code, 'wb') as imf:
        imf.write(img.content)
        pbar.update(1)


class AistBase:
    def __init__(self):
        pass

    @staticmethod
    def api(api_name, data):
        uri = 'http://sd.treee.com.cn/%s' % api_name
        response = requests.post(uri, data=data)
        return json.loads(response.text)


class Download(AistBase):
    def __init__(self, key):
        self.key = key
        self.get_image = get_image_pool

    def all(self, save_path):
        if os.path.exists(save_path) is False:
            print('Error: path is not existed.')
            return -1

        file_list = os.listdir(save_path)
        hash_list = []
        for f in file_list:
            hash_list.append(etag(join(save_path, f)))

        count = self.api('download', {'key': self.key, 'method': 'count'})
        total_image_number = int(count['total'])
        total_page = int(count['page'])

        total_size = 0
        with tqdm(total=total_image_number, unit='Pic') as pbar:
            pbar.set_description("Download")

            for p in range(total_page):
                image_info = self.api('download', {'key': self.key, 'method': 'download', 'page': p})
                image_code_list = image_info['image_code']
                image_hash_list = image_info['image_hash']
                image_size_list = image_info['image_size']
                image_url_list = image_info['image_url']
                image_download_args = []

                for i in range(len(image_url_list)):
                    total_size += image_size_list[i]
                    if image_hash_list[i] in hash_list:
                        pbar.update(1)
                        continue

                    image_download_args.append({'image_code': join(save_path, image_code_list[i]),
                                                'image_hash': image_hash_list[i],
                                                'image_url': image_url_list[i],
                                                'pbar': pbar})
                pool = Pool(cpu_count() - 1)
                pool.map(self.get_image, image_download_args)
                pool.close()
                pool.join()
        time.sleep(0.1)
        print('Total picture number: %d, total size: %6.2f MB' % (total_image_number, total_size / 1024.0 / 1024.0))
        return total_image_number

    def ls(self, list_file=''):
        count = self.api('download', {'key': self.key, 'method': 'count'})
        total_page = int(count['page'])
        image_list = []
        for p in range(total_page):
            image_info = self.api('download', {'key': self.key, 'method': 'ls', 'page': p})
            image_code_list = image_info['image_code']
            image_size_list = image_info['image_size']
            image_wx_openid_list = image_info['wx_openid']

            for i in range(len(image_code_list)):
                image_list.append({'image_name': image_code_list[i],
                                   'image_size': image_size_list[i],
                                   'contributor': image_wx_openid_list[i]})
        with open(list_file, 'w') as f:
            for im in image_list:
                f.write('%s,%d,%s\n' % (im['image_name'], im['image_size'], im['contributor']))
        return image_list
