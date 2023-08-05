# -*- coding: utf-8 -*-
# @Time    : 2019/11/14 14:45
# @E-Mail  : aberstone.hk@gmail.com
# @File    : cabinet_spider.py
# @Software: PyCharm
import scrapy
from scrapy_cabinet.utils import load_object


class Spider(scrapy.Spider):

    custom_settings = {
        "list_key": '',
        "url_key": '',
        "title_key": '',
        "key_map": dict(),
        "extract_type": "scrapy_cabinet.constants.ExtractType.LIST",
        "target_cls": ""
    }

    def prepare(self, *args, **kwargs):
        return args[0].text

    def parse(self, response):
        item = dict()
        item['need_extract'] = load_object(self.crawler.settings.get("extract_type"))
        item['target_cls'] = load_object(self.crawler.settings.get("target_cls"))
        item['source_page'] = self.prepare(response)
        yield item
