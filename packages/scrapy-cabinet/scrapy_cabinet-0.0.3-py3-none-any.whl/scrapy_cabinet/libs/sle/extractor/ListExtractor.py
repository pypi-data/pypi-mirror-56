# -*- coding: utf-8 -*-
# @Time    : 2019/11/8 11:06
# @E-Mail  : aberstone.hk@gmail.com
# @File    : ListExtractor.py
# @Software: PyCharm
import json
import re
from typing import re as Regex
from typing import Union, Dict, Sequence, AnyStr, List

from jsonpath import jsonpath
from lxml.html import HtmlElement

from scrapy_cabinet.libs.sle.extractor import TimeExtractor, TitleExtractor, URLExtractor
from scrapy_cabinet.utils import LOGGER

from scrapy_cabinet.libs.defaults import LIST_PATTERN_XPATH, LIST_PATTERN_RE
from scrapy_cabinet.libs.utils import pre_parse


class ListExtractor(object):
    def __init__(self, list_key: str = "", list_lambda: list = list()):
        self.list_pattern_re: List[Regex] = [re.compile(i, re.DOTALL) for i in LIST_PATTERN_RE]
        self.list_pattern_xpath = LIST_PATTERN_XPATH
        self.list_key = list_key
        self.list_lambda = list_lambda

    def _json_extractor(self, json_dict: Union[Dict, Sequence]) -> List:
        r_list: List[List, Dict, AnyStr] = []
        if self.list_key:
            r_list = jsonpath(json_dict, self.list_key)
            LOGGER.info(
                "PATTERN_TYPE: {} || PATTERN: {} || RESULT: {}".format(
                    "list_default",
                    self.list_key,
                    "length: " + str(len(r_list))
                )
            )
        else:
            _ = list(filter(lambda x: isinstance(x, list), jsonpath(json_dict, "$..")))
            if len(_) > 0:
                r_list = max(_, key=lambda x: len(x))
                LOGGER.info(
                    "PATTERN_TYPE: {} || PATTERN: {} || RESULT: {}".format(
                        "list_default",
                        "None",
                        "length: " + str(len(r_list))
                    )
                )
        return r_list

    def _xpath_extractor(self, element: HtmlElement) -> List[HtmlElement]:
        r_list: List[HtmlElement] = []
        if self.list_key:
            r_list = element.xpath(self.list_key)
            LOGGER.info(
                "PATTERN_TYPE: {} || PATTERN: {} || RESULT: {}".format(
                    "list_default",
                    self.list_key,
                    "length: " + str(len(r_list))
                )
            )
        else:
            for xpath_str in self.list_pattern_xpath:
                r_list = element.xpath(xpath_str)
                if r_list:
                    LOGGER.info(
                        "PATTERN_TYPE: {} || PATTERN: {} || RESULT: {}".format(
                            "list_default",
                            xpath_str,
                            "length: " + str(len(r_list))
                        )
                    )
                    return r_list
        return r_list

    def _regex_extractor(self, source) -> List[AnyStr]:
        _: List[AnyStr] = []
        if "<" in self.list_key:
            _ = list(filter(lambda x: x, re.findall(self.list_key, source, re.DOTALL)))
        else:
            for re_pattern in self.list_pattern_re:
                _r = list(filter(lambda x: x, re_pattern.findall(source)))
                if _r:
                    LOGGER.info(
                        "PATTERN_TYPE: {} || PATTERN: {} || RESULT: {}".format(
                            "list_default",
                            re_pattern,
                            "length: " + str(len(_r))
                        )
                    )
                    return _r
        if _:
            LOGGER.info(self.list_key)
        return _

    def _extractor(self, source: Union[Dict, Sequence, HtmlElement, AnyStr]) -> List[HtmlElement or Dict]:
        try:
            source = json.loads(source)
        except Exception as e:
            LOGGER.info("SOURCE IS NOT JSON FORMAT: {} || TRY XPATH AND REGEX".format(e))
            pass
        if isinstance(source, (HtmlElement, str)):
            # regex
            if isinstance(source, str):
                _ = self._regex_extractor(source)
                if _:
                    return _
            # xpath
            source = pre_parse(source)
            return self._xpath_extractor(source)
        # jsonpath
        return self._json_extractor(source)

    def extractor(self, source: Union[Dict, Sequence, HtmlElement, AnyStr]) -> List[HtmlElement or Dict]:
        _ = self._extractor(source)
        for fn in self.list_lambda:
            _ = eval(fn)(_)
        return _


if __name__ == '__main__':
    with open("resutl", "r") as f:
        r = f.read()
    extractor = ListExtractor()
    r = extractor.extractor(r)
    for i in r:
        time_extractor = TimeExtractor()
        title_extractor = TitleExtractor()
        url_extractor = URLExtractor()
        # LOGGER.warning(i)
        title_extractor.extractor(i)
        time_extractor.extractor(i)
        url_extractor.extractor(i)
