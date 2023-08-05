# -*- coding: utf-8 -*-
# @Time    : 2019/11/7 15:54
# @E-Mail  : aberstone.hk@gmail.com
# @File    : constants.py
# @Software: PyCharm
from enum import Enum

class ExtractType(Enum):
    NEWS = 1
    LIST = 2

class ExtractorType(Enum):
    XPATH = 1
    JSONPATH = 2