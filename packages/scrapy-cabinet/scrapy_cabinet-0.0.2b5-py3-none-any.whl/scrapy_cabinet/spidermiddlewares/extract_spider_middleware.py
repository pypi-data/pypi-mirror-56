# -*- coding: utf-8 -*-
# @Time    : 2019/11/7 13:44
# @E-Mail  : aberstone.hk@gmail.com
# @File    : extract_spider_middleware.py
# @Software: PyCharm
from typing import Iterator, Dict, List

from scrapy import signals

from scrapy_cabinet.constants import ExtractType
from scrapy_cabinet.utils import LOGGER
from scrapy_cabinet.libs.gne import GeneralNewsExtractor
from scrapy_cabinet.libs.sle import SmartListInfoExtractor

from scrapy_cabinet.types import _Crawler, _Response, _Spider, _Result, _Request, _Item


class ExtractSpiderMiddleware(object):
    """A base DownloaderMiddleware to set proxy to Scrapy request.

    To use this Middleware, Project should set proxy_url or proxy_pool in settings.py.
    When use PROXY_URL, PROXY_TYPE should be set at the same time.
        PROXY_TYPE == 1 or PROXY_TYPE == 0.

    Attributes:
        proxies : _Proxies : A _Proxies type to store proxy_url.
        is_init : bool     : A bool value to check the proxies is set successfully

    Methods:
        get_proxies  | Args: NaN | A method to get proxy_url, when use proxy_url and proxy_type == 1
                                   this method can not be implemented.

    """

    def __init__(self, crawler: _Crawler):
        self.gne = GeneralNewsExtractor()
        self.sle = SmartListInfoExtractor(
            key_map  = crawler.settings.get("key_map", dict(url='url', time='time', title='title')),
            list_key = crawler.settings.get("list_key", ""),
            list_lambda  = crawler.settings.get("list_lambda",list()),
            time_key = crawler.settings.get("time_key", ""),
            time_lambda=crawler.settings.get("time_lambda",list()),
            title_key= crawler.settings.get("title_key", ""),
            title_lambda=crawler.settings.get("title_lambda", list()),
            url_key  = crawler.settings.get("url_key", ""),
            url_lambda=crawler.settings.get("url_lambda", list()),
        )

    @classmethod
    def from_crawler(cls, crawler: _Crawler) -> object:
        # This method is used by Scrapy to create your spiders.
        s = cls(crawler)
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response: _Response, spider: _Spider) -> None:
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response: _Response, result: _Result, spider: _Spider) -> _Result:
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            if isinstance(i, dict) and i.get("need_extract"):
                r = self.extract(i, response, i['need_extract'])
                for t in r:
                    yield t
            yield i

    def process_spider_exception(self, response: _Response, exception: Exception, spider: _Spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests: Iterator[_Request], spider: _Spider) -> Iterator[_Request]:
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider: _Spider):
        spider.logger.info('Spider opened: %s' % spider.name)

    def extract(self, result: Dict, response: _Response, type: ExtractType) -> List[_Item]:
        target_cls = result['target_cls']
        source_page = result['source_page']
        i_list = []
        if type == ExtractType.NEWS:
            _result = self.gne.extract(source_page)
            item = target_cls()
            for k, v in _result.items():
                item[k] = v
            i_list.append(item)
        elif type == ExtractType.LIST:
            _result = self.sle.extract(source_page)
            for r in _result:
                item = target_cls()
                for k, v in r.items():
                    item[k] = v
                i_list.append(item)
        return i_list
