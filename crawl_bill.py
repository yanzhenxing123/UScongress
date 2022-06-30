import time

from selenium.common.exceptions import WebDriverException

import utils
from lxml import etree
import threading
from config import db
from loguru import logger
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By

sql_f = '''
        UPDATE `bill`
        SET `bill_raw_text` = {bill_raw_text}, 
            `cosponsor_names` = {cosponsor_names}
        WHERE `id` = {bill_id}
'''


class CrawlTread(threading.Thread):
    """
    爬虫消费者
    """

    def __init__(self):
        super(CrawlTread, self).__init__()
        self.mysql_conn = db.MysqlConn.get_conn()
        self.redis_conn = db.Redis.get_conn()
        self.driver = utils.get_driver()

    def run(self):
        """
        线程要运行的代码
        :return:
        """
        count = 0
        while True:
            bill_id_and_url_str = self.redis_conn.brpop("bill_url")[1]
            bill_id, bill_url = bill_id_and_url_str.split(",")

            try:
                # redis获取bill_url
                bill_text_url = bill_url + '/text'
                # 先请求bill_text
                self.driver.get(bill_text_url)
                if count == 0:
                    time.sleep(6)
                time.sleep(2.5)
                bill_text_html = etree.HTML(self.driver.page_source)
                bill_raw_text = "'" + "".join(
                    bill_text_html.xpath("//div[@class='generated-html-container ']//text()")) \
                    .replace("'", "") + "'"
                # 请求bill_cosponsor
                bill_cosponsor_element = self.driver.find_element(By.XPATH,
                                                                  value="//body/div[@id='container']/div[1]/main[1]/nav[1]/ul[1]/li[6]/h2[1]/a[1]")
                bill_cosponsor_element.click()
                time.sleep(1.5)
                bill_cosponsor_html = etree.HTML(self.driver.page_source)
                cosponsor_names = bill_cosponsor_html.xpath("//td[@class='actions']/a/text()")
                cosponsor_names_str = "'" + str(cosponsor_names).replace("'", "") + "'" if cosponsor_names else "''"

            except WebDriverException as ex:
                logger.error("WebDriver异常" + ex.__str__())
                self.driver.quit()
                self.driver = utils.get_driver()
                break
            except Exception as e:
                cosponsor_names_str = "''"
                logger.error("cosponsor_names 获取异常: " + e.__str__())

            self.insert(bill_raw_text, cosponsor_names_str, bill_id)
            count += 1

    def insert(self, bill_raw_text: str, cosponsor_names_str: str, bill_id: str):
        """
        更新数据库
        :param bill_raw_text:
        :param cosponsor_names_str:
        :param bill_id:
        :return:
        """

        sql = sql_f.format(bill_raw_text=bill_raw_text,
                           cosponsor_names=cosponsor_names_str,
                           bill_id=bill_id)
        self.mysql_conn.ping(reconnect=True)
        cursor = self.mysql_conn.cursor()
        try:
            if cursor.execute(sql):
                logger.success(f"插入{bill_id}成功")
                self.mysql_conn.commit()
                # 删除bill_id
                self.redis_conn.delete("bill_url_" + bill_id)
        except Exception as e:
            logger.error(f"插入{bill_id}失败, 原因: {e.__str__()}")
            logger.info(sql)
        finally:
            cursor.close()


if __name__ == '__main__':
    treads = []
    nums = 3
    for _ in range(nums):
        c_thread = CrawlTread()
        c_thread.start()
        treads.append(c_thread)
    for c_thread in treads:
        c_thread.join()
