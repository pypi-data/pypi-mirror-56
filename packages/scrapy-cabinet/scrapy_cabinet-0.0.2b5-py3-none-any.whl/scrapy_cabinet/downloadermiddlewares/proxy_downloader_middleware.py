# -*- coding: utf-8 -*-
# @Time    : 2019/11/6 10:15
# @E-Mail  : aberstone.hk@gmail.com
# @File    : ProxyDownloaderMiddleware.py
# @Software: PyCharm
import random
from typing import Optional

from scrapy import signals

from scrapy_cabinet.exceptions import NotSetProxyError
from scrapy_cabinet.utils import LOGGER
from scrapy_cabinet.types import _Proxies, _Crawler, _Spider, _Request


class ProxyDownloaderMiddleware(object):
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

    def __init__(self, proxies: _Proxies) -> None:
        self.proxies: _Proxies = proxies
        self.is_init = True

    @classmethod
    def from_crawler(cls, crawler: _Crawler) -> object:
        o = None
        proxies = crawler.settings.get("PROXY_URL")
        if proxies:
            proxies_type = crawler.settings.get("PROXY_TYPE")
            if proxies_type == 0:
                o = cls(proxies)
                o.proxies = o.get_proxies()
            else:
                o = cls(proxies)

        # 说明没有proxy_url,寻找代理池

        proxies = crawler.settings.get("PROXY_POOL")
        if proxies:
            LOGGER.warning(
                "THIS PROXY_POOL WILL BE DROPED IN A FUTURE VERSION, PLEASE USE PROXY_URL and IMPLEMENT get_proxies method")
            o = cls(proxies)
        if o:
            crawler.signals.connect(o.spider_opened, signal=signals.spider_opened)
            return o
        # ERROR
        LOGGER.error("TO USE THIS MIDDLEWARE ,PLEASE SET PROXY_URL OR PROXY_POOL")
        raise NotSetProxyError()

    def spider_opened(self, spider: _Spider) -> None:
        spider.logger.info(f"Proxy Has Been Set. Type: {type(self.proxies)}")

    def process_request(self, request: _Request, spider: _Spider) -> None:
        if isinstance(self.proxies, list):
            proxies = random.choice(self.proxies)
        else:
            proxies = self.proxies
        request.meta["proxy"] = proxies
        spider.logger.debug(f"{proxies}")

    def get_proxies(self) -> Optional[_Proxies]:
        raise NotImplementedError()
