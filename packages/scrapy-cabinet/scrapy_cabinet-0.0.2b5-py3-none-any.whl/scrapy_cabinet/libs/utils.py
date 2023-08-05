import re
from typing import Dict

from scrapy_cabinet.utils import LOGGER

from scrapy_cabinet.libs.defaults import USELESS_TAG, TAGS_CAN_BE_REMOVE_IF_EMPTY, USELESS_ATTR
from lxml.html import fromstring, HtmlElement
from lxml.html import etree


def normalize_node(element: HtmlElement):
    for node in iter_node(element):
        if node.tag.lower() in USELESS_TAG:
            remove_node(node)

        # inspired by readability.
        if node.tag.lower() in TAGS_CAN_BE_REMOVE_IF_EMPTY and is_empty_element(node):
            remove_node(node)

        # p 标签下面的 span 标签中的文字，可以合并到 p 标签中
        if node.tag.lower() == 'p':
            etree.strip_tags(node, 'span')
            etree.strip_tags(node, 'strong')

        # li标签下的span中的文字，可以替换
        if node.tag.lower() == 'li':
            pass
        if node.tag.lower() in ['b']:
            node.tag = 'p'

        # if a div tag does not contain any sub node, it could be converted to p node.
        if node.tag.lower() == 'div' and not node.getchildren():
            node.tag = 'p'

        if node.tag.lower() == 'span' and not node.getchildren():
            node.tag = 'p'

        class_name = node.get('class')
        if class_name:
            for attribute in USELESS_ATTR:
                if attribute in class_name:
                    remove_node(node)
                    break


def pre_parse(html):
    if isinstance(html, str):
        html = re.sub('</?br.*?>', '', html)
        html = fromstring(html)
    normalize_node(html)
    return html


def remove_noise_node(element, noise_xpath_list):
    if not noise_xpath_list:
        return
    for noise_xpath in noise_xpath_list:
        nodes = element.xpath(noise_xpath)
        for node in nodes:
            remove_node(node)
    return element


def iter_node(element: HtmlElement):
    yield element
    for sub_element in element:
        if isinstance(sub_element, HtmlElement):
            yield from iter_node(sub_element)


def remove_node(node: HtmlElement):
    """
    this is a in-place operation, not necessary to return
    :param node:
    :return:
    """
    parent = node.getparent()
    if parent is not None:
        parent.remove(node)


def is_empty_element(node: HtmlElement):
    return not node.getchildren() and not node.text


def one_layer_dict(source: Dict, key: str = ""):
    _ = {}
    for k, v in source.items():
        if isinstance(v, Dict):
            _.update(one_layer_dict(v, key + k + "_"))
            # key = key + "_" + k
        else:
            _[key + k] = v
    return _


if __name__ == '__main__':
    a = {
        "a": {
            "b": 2,
            "c": {
                "dd": 1,
                "abc": "asdasd"
            }
        },
        "d": 4
    }
    a = one_layer_dict(a)
    print(a)
    # for i in a:
    #     print(i)
