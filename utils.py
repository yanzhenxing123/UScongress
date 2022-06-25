"""
@Author: yanzx
@Date: 2022/5/19 23:13
@Description: 
"""
import os
import re
from typing import Dict
from urllib.parse import quote, unquote

root_url = "https://www.congress.gov"


def get_project_path():
    """
    得到项目路径
    """
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
    """
    匹配tracker中的数据
    :param item_element:
    :return:
    """
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
    """
    过滤文章数据
    :param text:
    :return:
    """
    res = text.replace('\\u2014', '')
    return res


def format_dataset(data: Dict):
    """
    对要插入bill的数据进行格式化
    :param data:
    :return:
    """
    data.pop('bill_id')  # 删除 bill_id字段
    data['members'] = data.pop('member')  # 用members代替member
    for key, value in data.items():
        if isinstance(value, list):
            data[key] = str(value)
        else:
            data[key] = value
    return data


def get_driver_executable_path():
    return get_project_path() + '\\config\\chromedriver.exe'


if __name__ == '__main__':
    url = "https://www.congress.gov/search?q=%7B%22congress%22%3A%5B%22117%22%5D%2C%22source%22%3A%22all%22%2C%22search%22%3A%22health+care%22%2C%22bill-status%22%3A%5B%22introduced%22%2C%22committee%22%2C%22floor%22%2C%22failed-one%22%2C%22passed-one%22%5D%7D"
    url = "https://www.congress.gov/advanced-search/legislation?congresses%5B%5D=117&legislationNumbers=&restrictionType=field&restrictionFields%5B%5D=allBillTitles&restrictionFields%5B%5D=summary&summaryField=billSummary&enterTerms=health+care&wordVariants=true&legislationTypes%5B%5D=hr&legislationTypes%5B%5D=hres&legislationTypes%5B%5D=hjres&legislationTypes%5B%5D=hconres&legislationTypes%5B%5D=hamdt&legislationTypes%5B%5D=s&legislationTypes%5B%5D=sres&legislationTypes%5B%5D=sjres&legislationTypes%5B%5D=sconres&legislationTypes%5B%5D=samdt&public=true&private=true&chamber=all&actionTerms=&legislativeActionWordVariants=true&dateOfActionOperator=equal&dateOfActionStartDate=&dateOfActionEndDate=&dateOfActionIsOptions=yesterday&dateOfActionToggle=multi&legislativeAction=Any&sponsorState=One&member=&sponsorTypes%5B%5D=sponsor&sponsorTypeBool=OR&dateOfSponsorshipOperator=equal&dateOfSponsorshipStartDate=&dateOfSponsorshipEndDate=&dateOfSponsorshipIsOptions=yesterday&committeeActivity%5B%5D=0&committeeActivity%5B%5D=3&committeeActivity%5B%5D=11&committeeActivity%5B%5D=12&committeeActivity%5B%5D=4&committeeActivity%5B%5D=2&committeeActivity%5B%5D=5&committeeActivity%5B%5D=9&satellite=%5B%5D&search=&submitted=Submitted"
    url = "https://www.congress.gov/advanced-search/legislation?congresses%5B0%5D=117&legislationNumbers=&restrictionType=field&restrictionFields%5B0%5D=allBillTitles&restrictionFields%5B1%5D=summary&summaryField=billSummary&enterTerms=health+care&wordVariants=true&legislationTypes%5B0%5D=hr&legislationTypes%5B1%5D=hres&legislationTypes%5B2%5D=hjres&legislationTypes%5B3%5D=hconres&legislationTypes%5B4%5D=hamdt&legislationTypes%5B5%5D=s&legislationTypes%5B6%5D=sres&legislationTypes%5B7%5D=sjres&legislationTypes%5B8%5D=sconres&legislationTypes%5B9%5D=samdt&public=true&private=true&chamber=all&actionTerms=&legislativeActionWordVariants=true&dateOfActionOperator=equal&dateOfActionStartDate=&dateOfActionEndDate=&dateOfActionIsOptions=yesterday&dateOfActionToggle=multi&legislativeAction=Any&sponsorState=One&member=&sponsorTypes%5B0%5D=sponsor&sponsorTypeBool=OR&dateOfSponsorshipOperator=equal&dateOfSponsorshipStartDate=&dateOfSponsorshipEndDate=&dateOfSponsorshipIsOptions=yesterday&committeeActivity%5B0%5D=0&committeeActivity%5B1%5D=3&committeeActivity%5B2%5D=11&committeeActivity%5B3%5D=12&committeeActivity%5B4%5D=4&committeeActivity%5B5%5D=2&committeeActivity%5B6%5D=5&committeeActivity%5B7%5D=9&satellite=%5B%5D&search=&submitted=Submitted&q=%7B%22bill-status%22%3A%22introduced%22%2C%22party%22%3A%5B%22Democratic%22%2C%22Republican%22%5D%7D"
    url = "https://www.congress.gov/advanced-search/legislation?congresses%5B0%5D=117&legislationNumbers=&restrictionType=field&restrictionFields%5B0%5D=allBillTitles&restrictionFields%5B1%5D=summary&summaryField=billSummary&enterTerms=&wordVariants=true&legislationTypes%5B0%5D=hr&legislationTypes%5B1%5D=hres&legislationTypes%5B2%5D=hjres&legislationTypes%5B3%5D=hconres&legislationTypes%5B4%5D=hamdt&legislationTypes%5B5%5D=s&legislationTypes%5B6%5D=sres&legislationTypes%5B7%5D=sjres&legislationTypes%5B8%5D=sconres&legislationTypes%5B9%5D=samdt&public=true&private=true&chamber=all&actionTerms=health%0D%0A&legislativeActionWordVariants=true&dateOfActionOperator=equal&dateOfActionStartDate=&dateOfActionEndDate=&dateOfActionIsOptions=yesterday&dateOfActionToggle=multi&legislativeAction=Any&sponsorState=One&member=&sponsorTypes%5B0%5D=sponsor&sponsorTypeBool=OR&dateOfSponsorshipOperator=equal&dateOfSponsorshipStartDate=&dateOfSponsorshipEndDate=&dateOfSponsorshipIsOptions=yesterday&committeeActivity%5B0%5D=0&committeeActivity%5B1%5D=3&committeeActivity%5B2%5D=11&committeeActivity%5B3%5D=12&committeeActivity%5B4%5D=4&committeeActivity%5B5%5D=2&committeeActivity%5B6%5D=5&committeeActivity%5B7%5D=9&satellite=%5B%5D&search=&submitted=Submitted&q=%7B%22bill-status%22%3A%5B%22introduced%22%2C%22floor%22%2C%22failed-one%22%2C%22passed-one%22%2C%22passed-both%22%2C%22resolving%22%2C%22president%22%2C%22law%22%5D%7D"
    print(unquote_text(url))