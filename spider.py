"""
@Author: yanzx
@Date: 2022/5/18 23:03
@Description: main函数
"""
import re
from selenium.webdriver.common.by import By
import utils
import time
from lxml import etree
import undetected_chromedriver as uc
from typing import Dict, Optional
from loguru import logger
from models.models import URLModel, URL, DataSet

options = uc.ChromeOptions()
# 线程池
ROOT_PATH = utils.get_project_path()


class Spider:
    """
    Spider类
    """

    def __init__(self, url_data: Dict):
        self.driver = utils.get_driver()
        self.url_data = url_data
        self.url = self.get_url(self.url_data)
        self.count = 0
        self.page_count = 0
        self.max_count = 100

    def get_url(self, url_data: Dict) -> str:
        """
        获取url
        :param url_data:
        :return:
        """
        url_model = URLModel(**url_data)
        url = URL(url_model).get_url()
        logger.info(url)
        return url

    def run(self, max_num=200):
        """
        发送请求
        :return:
        """
        self.driver.get(self.url)
        delay = 10
        time.sleep(delay)
        # 法案点进去
        while True:
            time.sleep(5)
            self.page_count += 1
            text = self.driver.page_source
            html = etree.HTML(text)
            logger.info(f"正在爬取第{self.page_count}页...")
            # 解析并插入数据
            self.parse_all(html)
            if self.count == max_num:
                logger.info(" 爬取已完成 done~~~~")
                self.driver.quit()
                break
            next = self.driver.find_element(by=By.XPATH, value="//a[@class='next'][last()]")
            if not next or self.page_count >= self.max_count:
                logger.info("====== 没找到下一页 ======")
                self.driver.quit()
                break
            next.click()
            time.sleep(delay)

    def parse_all(self, html):
        """
        解析整个页面的html
        :param html:
        :return:
        """
        main_element = html.xpath("//div[@id='main']")[0]
        item_elements = main_element.xpath("./ol/li[@class='expanded']")
        for i in range(len(item_elements)):
            # 解析
            item = self.parse_item(item_elements[i])
            # 插入数据库
            self.insert(item, self.url_data)
        # self.crawl_bill_txt_and_cosponsors()

    def parse_item(self, item_element):
        """
        解析一个item
        :param item_element:
        :return:
        """
        # 单个法案信息
        item = {}
        # 法案的id, 搜索后排序的id
        bill_id = "".join(item_element.xpath("./text()"))
        bill_id = re.findall(r'\d+', bill_id)[0]
        # 法案的heading, eg:  H.R.6776 — 117th Congress (2021-2022)
        heading_text = item_element.xpath(".//span[@class='result-heading']//text()")
        heading = "".join(heading_text)
        # 法案的bill_url, 详细信息
        bill_url = item_element.xpath(".//span[@class='result-heading']/a/@href")

        bill_url = utils.format_url(bill_url[0]) if bill_url else ''
        # 法案的title, eg: Health Care Worker and First Responder Social Security Beneficiary Choice Act of 2022
        title_text = item_element.xpath(".//span[@class='result-title']//text()")
        title = "".join(title_text)
        # 法案的类型 eg: BILL、RESOLUTION、...
        type = item_element.xpath(".//span[@class='visualIndicator']/text()")[0]
        # 法案的进程
        tracker = utils.match_tracker(item_element)
        item['bill_id'] = bill_id
        item['type'] = type
        item['tracker'] = tracker
        item['heading'] = heading
        item['bill_url'] = bill_url
        item['title'] = title

        # Sponsor Committees Latest_Action
        result_item_elements = item_element.xpath(".//span[@class='result-item']")
        for result_item_element in result_item_elements:
            keys = result_item_element.xpath("./strong/text()")
            values = result_item_element.xpath(".//text()")
            for key in keys:
                index = values.index(key) + 1
                if key == 'Sponsor:':
                    index_Cosponsors = values.index('Cosponsors:')
                    value = "".join(values[index: index_Cosponsors])
                    Sponsor_url = result_item_element.xpath('./a[1]/@href')[0]
                    Sponsor_url = utils.format_url(Sponsor_url)
                    item['Sponsor_url'] = Sponsor_url
                else:
                    value = "".join(values[index:])
                    # 如果是贡献者，那么将其余部分去掉
                    if key == 'Cosponsors:':
                        try:
                            value = re.findall(r'\d+', value)[0]
                        except Exception:
                            value = 0
                item[key[:-1]] = value
        # utils.print_dict(item)
        return item

    def insert(self, bill: Dict, url_data: Dict):
        """
        插入数据库: 单个插入后面可优化
        :param bills:
        :param url_model:
        :return:
        """
        dataset_data = {**bill, **url_data}
        dataset = DataSet(**dataset_data)
        dataset.insert()
        self.count += 1
        if self.count % 50 == 0 and self.count != 0:
            logger.info(f"已经插入了{self.count}条数据...")


def main(data: Optional[Dict]):
    """
    main函数
    :return:
    """
    spider = Spider(data)
    spider.run(data['crawl_nums'])


if __name__ == '__main__':
    data = {
        'congress_group': 1,
        'congress': None,
        'member': None,
        'legislationNumbers': None,
        'enterTerms': 'health care',
        'actionTerms': 8000,
        'satellite': None,
        'crawl_nums': 200
    }
    main(data)
