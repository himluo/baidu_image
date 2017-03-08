# -*- coding: utf-8 -*-
import scrapy
import time
import json
from baidu_image.items import BaiduImageItem
import re


class ImageSpider(scrapy.Spider):
    name = "image"

    def start_requests(self):
        keyword = getattr(self, 'keyword', None)
        start_num = getattr(self, 'start', 0)
        amount = getattr(self, 'amount', 30)
        #now = int(time.time() * 1000)

        #url = 'https://image.baidu.com/search/acjson?tn=resultjson_com&ipn=rj&ct=201326592&is=&fp=result&queryWord=%s&cl=2&lm=-1&ie=utf-8&oe=utf-8&adpicid=&st=-1&z=&ic=&word=%s&s=&se=&tab=&width=&height=&face=&istype=&qc=&nc=1&fr=&pn=%s&rn=%s&gsm=1e&%d=' % (keyword, keyword, start_num, amount, now)
        url = 'https://image.baidu.com/search/acjson?tn=resultjson_com&ipn=rj&ie=utf-8&oe=utf-8&word=%s&pn=%s&rn=%s' % \
              (keyword, start_num, amount)
        yield scrapy.Request(url, callback=self.parse)


    def parse(self, response):
        c = response.body.decode(encoding='utf-8').replace(r'<\/strong>', '').replace('<strong>', '').replace(r'\'', '')
        jbody = json.loads(c)
        jdata = jbody['data']
        item = BaiduImageItem()
        for image in jdata:
            if 'objURL' in image:
                item['image_urls'] = [self.decode_url(image['objURL'])]
                yield item

    def decode_url(self, url):
        dict_code = {
            'w': 'a', 'k': 'b', 'v': 'c', '1': 'd', 'j': 'e', 'u': 'f', '2': 'g', 'i': 'h',
            't': 'i', '3': 'j', 'h': 'k', 's': 'l', '4': 'm', 'g': 'n', '5': 'o', 'r': 'p',
            'q': 'q', '6': 'r', 'f': 's', 'p': 't', '7': 'u', 'e': 'v', 'o': 'w',
            '8': '1', 'd': '2', 'n': '3', '9': '4', 'c': '5', 'm': '6', '0': '7', 'b': '8', 'l': '9',
            'a': '0', '_z2C$q': ':', '_z&e3B': ".", 'AzdH3F': '/'
        }

        url_list = re.compile('(_z2C\\$q|_z&e3B|AzdH3F|.)').findall(url)
        return ''.join([dict_code.get(key, key) for key in url_list])



