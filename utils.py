"""
@Author: yanzx
@Date: 2022/5/19 23:13
@Description: 
"""
import os
import re
from typing import Dict
from urllib.parse import quote, unquote

root_url = "https://www.congress.gov/"


def get_project_path():
    """得到项目路径"""
    project_path = os.path.join(
        os.path.dirname(__file__), "."
    )
    return project_path


def print_dict(data: Dict):
    """
    格式化输出字典
    :param data:
    :return:
    """
    for key, value in data.items():
        print(str(key) + ': ' + str(value))
    print("*" * 100)


def format_url(url: str):
    """
    匹配 url，将 ?q=后面的去掉
    :param url: 原始url
    :return: 匹配后的url
    """
    try:
        url = re.search('(.*?)(\?)', url).group(1)
    except Exception:
        url = url
    if url:
        return root_url + url
    return url


def quote_text(text: str):
    """
    url编码
    :param text:
    :return:
    """
    return quote(text, 'utf-8')


def unquote_text(text: str):
    """
    url解码
    :param text:
    :return:
    """
    return unquote(text, 'utf-8')


def match_tracker(item_element):
    tracker1 = item_element.xpath(".//span[@class='result-item result-tracker']//li[@class='selected']/text()")
    tracker2 = item_element.xpath(".//span[@class='result-item result-tracker']//li[@class='selected last']/text()")
    tracker3 = item_element.xpath(
        ".//span[@class='result-item result-tracker']//li[@class='selected mediumTrack last']/text()")
    trackers = [tracker1, tracker2, tracker3]

    if any(trackers):
        trackers = map(str, trackers)
        tracker = "".join(trackers).replace('[', '').replace(']', '').replace('\'', '')
    else:
        tracker = None
    return tracker


def filter_text(text: str):
    res = text.replace('\\u2014', '')
    return res


def url_intput_orders():
    pass
