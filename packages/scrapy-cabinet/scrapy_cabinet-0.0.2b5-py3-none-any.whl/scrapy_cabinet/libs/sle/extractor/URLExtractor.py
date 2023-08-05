# -*- coding: utf-8 -*-
# @Time    : 2019/11/13 17:48
# @E-Mail  : aberstone.hk@gmail.com
# @File    : URLExtractor.py
# @Software: PyCharm
import json
import re
from functools import reduce
from typing import Union, Dict, List, AnyStr

from jsonpath import jsonpath
from lxml.html import HtmlElement
from lxml.etree import tostring
from scrapy_cabinet.utils import LOGGER

from scrapy_cabinet.libs.defaults import URL_PATTERN_XPATH, URL_JSON_KEYS, URL_PATTERN
from scrapy_cabinet.libs.utils import pre_parse, one_layer_dict


class URLExtractor(object):
    def __init__(self, url_key: str = "", url_lambda: list = list()):
        self.url_xpath_pattern = URL_PATTERN_XPATH
        self.url_key = url_key
        self.url_pattern = URL_PATTERN
        self.url_lambda = url_lambda

    def _json_extractor(self, json_dict: Union[Dict, List]):
        text = ""
        if self.url_key and "$" in self.url_key:
            text = "".join(jsonpath(json_dict, self.url_key))
            LOGGER.info(
                "PATTERN_TYPE: {} || PATTERN: {} || RESULT: {}".format(
                    "time_args",
                    self.url_key,
                    text
                )
            )
        elif self.url_key:
            r = reduce(lambda x, y: x + y, re.findall(self.url_key, json.dumps(json_dict), re.DOTALL))
            r = max(r, key=lambda x: len(x))
            if r:
                LOGGER.info(
                    "PATTERN_TYPE: {} || PATTERN: {} || RESULT: {}".format(
                        "url_key_regex",
                        self.url_key,
                        r
                    )
                )
                return r
        else:
            tmp = one_layer_dict(json_dict)
            keys_default_list = [URL_JSON_KEYS for _ in range(len(tmp))]
            for i in filter(
                    lambda x: any([i in x[0].lower() for i in x[1]]) and tmp[x[0]],
                    zip(tmp.keys(), keys_default_list)
            ):
                text = tmp[i[0]]
                break
            if text:
                LOGGER.info(
                    "PATTERN_TYPE: {} || PATTERN: {} || RESULT: {}".format(
                        "url_default",
                        "url in dict.keys",
                        text
                    )
                )
        return text

    def _xpath_extractor(self, element: HtmlElement):
        if self.url_key:
            text = "".join(element.xpath(self.url_key))
            # LOGGER
            LOGGER.info("PATTERN_TYPE: {} || PATTERN: {} || RESULT: {}".format("url_args", self.url_key, text))
            return text
        _ = tostring(element).decode()
        for dt in self.url_pattern:
            text = re.search(dt, _)
            if text:
                text = text.group(1)
                # LOGGER
                LOGGER.info("PATTERN_TYPE: {} || PATTERN: {} || RESULT: {}".format("url_default", dt, text))
                return text

    def _extractor(self, source: Union[Dict, List, HtmlElement, AnyStr]) -> str:
        if isinstance(source, (HtmlElement, str)):
            source = pre_parse(source)
            return self._xpath_extractor(source)
        return self._json_extractor(source)

    def extractor(self, source: Union[Dict, List, HtmlElement, AnyStr]) -> str:
        _ = self._extractor(source)
        for fn in self.url_lambda:
            temp = list()
            temp.extend(_) if isinstance(_, list) else temp.append(_)
            _ = eval(fn)(*temp)
        return _
