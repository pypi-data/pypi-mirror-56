# -*- coding: utf-8 -*-
# @Time    : 2019/11/7 16:57
# @E-Mail  : aberstone.hk@gmail.com
# @File    : __init__.py.py
# @Software: PyCharm
from typing import Union, AnyStr, Dict
from lxml.html import HtmlElement
from scrapy_cabinet.utils import LOGGER

from scrapy_cabinet.libs.sle.extractor import TimeExtractor, ListExtractor, URLExtractor, TitleExtractor


class SmartListInfoExtractor(object):

    def __init__(
            self, key_map: Dict,
            list_key: str = "", list_lambda: list = list(),
            time_key: str = "", time_lambda: list = list(),
            title_key: str = "", title_lambda: list = list(),
            url_key: str = "", url_lambda: list = list()
    ):
        self.list_extractor = ListExtractor(list_key, list_lambda)
        self.time_extractor = TimeExtractor(time_key, time_lambda)
        self.url_extractor = URLExtractor(url_key, url_lambda)
        self.title_extractor = TitleExtractor(title_key, title_lambda)
        self.key_map = key_map

    def extract(self, html: Union[AnyStr, HtmlElement]):
        result = []
        list = self.list_extractor.extractor(html)

        for index, i in enumerate(list):
            # LOGGER.warning(index)
            result.append({
                self.key_map.get('url', 'url'): self.url_extractor.extractor(i),
                self.key_map.get('title', 'title'): self.title_extractor.extractor(i),
                self.key_map.get('time', 'time'): self.time_extractor.extractor(i)
            })

        return result
