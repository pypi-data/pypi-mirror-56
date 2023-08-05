# -*- coding: utf-8 -*-
# @Time    : 2019/11/6 15:35
# @E-Mail  : aberstone.hk@gmail.com
# @File    : redis_spider_idle_closed_extensions.py
# @Software: PyCharm
from scrapy import signals
from scrapy.exceptions import NotConfigured

from scrapy_cabinet.types import _Crawler, _Spider


class RedisSpiderIdleClosedExtensions(object):
    """A IdleClosed Extensions to close a idel RedisSpider.

    Attributes:
        crawler  : _Crawler : A _Crawler from Scrapy.
        idle_num : int      : A max wait times for idle.

    Methods:
        spider_idle  | spider: _Spider | A method when spider is idle, every 5 times check redis_key isEmpty.
    """

    def __init__(self, idle_num: int, crawler: _Crawler) -> None:
        self.crawler = crawler
        self.idle_num = idle_num
        self.idle_list = []
        self.idle_count = 0

    @classmethod
    def from_crawler(cls, crawler: _Crawler) -> object:
        if not crawler.settings.getbool('MYEXT_ENABLED'):
            raise NotConfigured
        if not 'redis_key' in crawler.spidercls.__dict__.keys():
            raise NotConfigured("ONLY SUPPORT REDISSPIDER")

        idle_num = crawler.settings.getint("IDLE_NUMBER", 120)
        ext = cls(idle_num, crawler)

        crawler.signals.connect(ext.spider_opened, signal=signals.spider_opened)
        crawler.signals.connect(ext.spider_closed, signal=signals.spider_closed)
        crawler.signals.connect(ext.spider_idle, signal=signals.spider_idle)

        return ext

    def spider_opened(self, spider: _Spider):
        spider.logger.info("opened spider {}, Allow waiting time:{} second".format(spider.name, self.idle_num * 5))

    def spider_closed(self, spider: _Spider):
        spider.logger.info("closed spider {}, Waiting time exceeded {} second".format(spider.name, self.idle_num * 5))

    def spider_idle(self, spider: _Spider):
        # 程序启动的时候会调用这个方法一次，之后每隔5秒再请求一次
        # 当持续10min都没有spider.redis_key，就关闭爬虫
        # 判断是否存在 redis_key
        if not spider.server.exists(spider.redis_key):
            self.idle_count += 1
        else:
            self.idle_count = 0

        if self.idle_count > self.idle_num:
            # 执行关闭爬虫操作
            self.crawler.engine.close_spider(spider, 'Waiting time exceeded')
