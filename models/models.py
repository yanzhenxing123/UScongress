"""
@Author: yanzx
@Date: 2022/5/26 23:17
@Description: 
"""
from pydantic import BaseModel, Field
from typing import List, Any, Dict

import utils
from config import db
from loguru import logger

conn = db.MysqlConn.get_conn()
redis = db.Redis.get_conn()


class URLModel(BaseModel):
    """
    URL模型类
    """

    congressGroup: List[int] = Field(None, description="{1973-2022, 1951-1972, 1799-1811, 1813-1873}, [0, 1, 2]")
    congresses: List[int] = Field(None, description="国会", alias='congresses[]')
    legislationNumbers: str = Field(None, description="eg: hr5")
    restrictionType: str = Field('field', description="restrictionType")
    restrictionFields: List[str] = Field(['allBillTitles', 'summary'], description='', alias='restrictionFields[]')
    summaryField: str = Field('billSummary', description='')
    enterTerms: str = Field(None, description='输入的关键词')
    legislationTypes: List[str] = Field(None, description='', alias='legislationTypes[]')
    public: bool = Field(True, description='')
    private: bool = Field(True, description='')
    wordVariants: bool = Field(True, description='')
    sponsorTypes: List[str] = Field(['sponsor'])
    committeeActivity: List[int] = Field(None)
    satellite: List = Field(None, alias='satellite')
    submitted: str = Field('Submitted', description='')
    member: str = Field(None, description='提出人')
    actionTerms: int = Field(None, description='法案所处的阶段 eg: 8000')

    # query中的数据
    query_party: List[str] = Field(None, description="party", alias="query_party[]")
    query_bill_status: List[str] = Field(None, description="bill_status", alias="query_bill-status[]")


class URL:
    """
    Advance Search URL拼接类
    """

    def __init__(self, url_model: URLModel):
        self.url_model = url_model
        self.base_url = "https://www.congress.gov/advanced-search/legislation?"

    def get_url(self):
        """
        获取拼接后的url
        :return:
        """
        res_li = []
        q = {}  # query
        url_dict = self.url_model.dict()
        for key, value in url_dict.items():
            value = url_dict.get(key)
            if not value:
                continue
            # 处理 q 字段
            elif key.startswith("query_"):
                if "bill_status" in key:
                    q['bill-status'] = value
                elif "party" in key:
                    q['party'] = value
            # 数组类型
            elif isinstance(value, List):
                key = key + "[]"
                for item in value:
                    res_li.append(key + "=" + str(item))
            # 常规类型
            else:
                res_li.append(key + "=" + str(value))
        if q:
            res_li.append("q=" + str(q).replace("'", '"'))
        res_str = "&".join(res_li)
        return self.base_url + res_str


class Bill(BaseModel):
    """
    法案类
    """
    bill_id: int = Field(None, description='')
    type: str = Field(None, description='')
    tracker: str = Field(None, description='')
    heading: str = Field(None, description='')
    bill_url: str = Field(None, description='')
    title: str = Field(None, description='')
    sponsor: str = Field(None, description='', alias='Sponsor')
    sponsor_url: str = Field(None, description='', alias='Sponsor_url')
    cosponsors: int = Field(None, description='', alias='Cosponsors')
    committees: str = Field(None, description='', alias='Committees')
    latest_action: Any = Field(None, description='', alias='Latest Action')

    def insert(self, table: str = 'bill'):
        """
        插入数据库
        :param table:
        :return:
        """
        data = self.dict()
        data.pop('bill_id')
        keys = ','.join(data.keys())
        values = ','.join(['%s'] * len(data))
        sql = 'INSERT INTO ' \
              '{table} ({keys}) ' \
              'VALUES({values})'.format(table=table, keys=keys, values=values)
        cursor = conn.cursor()
        if cursor.execute(sql, tuple(data.values())):
            conn.commit()


class DataSet(URLModel, Bill):
    """
    数据库类 = URLModel + Bill
    """

    def insert(self, table: str = 'bill'):
        """
        插入数据库
        :param table:
        :return:
        """
        data = self.dict()
        data = utils.format_dataset(data)
        keys = ','.join(data.keys())
        values = ','.join(['%s'] * len(data))
        sql = 'INSERT INTO ' \
              '{table} ({keys}) ' \
              'VALUES({values})'.format(table=table, keys=keys, values=values)
        cursor = conn.cursor()
        try:
            if cursor.execute(sql, tuple(data.values())):
                # 插入bill到redis
                self.insert_bill_url_to_redis(str(cursor.lastrowid), data)
                conn.commit()

        except Exception as e:
            logger.error(e.__str__())

    def insert_bill_url_to_redis(self, bill_id: str, data: Dict):
        """
        插入bill到redis
        :param bill_id:
        :param data:
        :return:
        """
        bill_url = data.get('bill_url')
        if bill_url:
            redis.lpush("bill_url", bill_id + "," + bill_url)
            # redis.set("bill_url_" + bill_id, bill_url)


class JsonResponse(object):
    """
    统一的json返回格式
    """

    def __init__(self, data, code, msg):
        self.data = data
        self.code = code
        self.msg = msg

    @classmethod
    def success(cls, data=None, code=200, msg='success'):
        return cls(data, code, msg)

    @classmethod
    def error(cls, data=None, code=-1, msg='error'):
        return cls(data, code, msg)

    def to_dict(self):
        return {
            "code": self.code,
            "msg": self.msg,
            "data": self.data
        }


if __name__ == '__main__':
    url_data = {
        'congressGroup': [0, 1],
        'congress': None,
        'member': None,
        'legislationNumbers': None,
        'enterTerms': 'health care',
        'actionTerms': 8000,
        'satellite': None,
    }

    bill_data = {
        'bill_id': '1', 'type': 'RESOLUTION', 'tracker': 'Agreed to in House',
        'heading': 'H.Res.838 — 117th Congress (2021-2022)',
        'bill_url': 'https://www.congress.gov//bill/117th-congress/house-resolution/838',
        'title': 'Providing for consideration of the bill (H.R. 5314) to protect our democracy by preventing abuses of presidential power, restoring checks and balances and accountability and transparency in government, and defending elections against foreign interference, and for other purposes; providing for consideration of the bill (S. 1605) to designate the National Pulse Memorial located at 1912 South Orange Avenue in Orlando, Florida, and for other purposes; and providing for consideration of the bill (S. 610) to address behavioral health and well-being among health care professionals.',
        'Sponsor_url': 'https://www.congress.gov//member/mary-scanlon/S001205',
        'Sponsor': ' Rep. Scanlon, Mary Gay [D-PA-5] (Introduced 12/07/2021) ', 'Cosponsors': '0',
        'Committees': ' House - Rules        ', 'Committee Report': ' H. Rept. 117-205        ',
        'Latest Action': "dda"
    }

    url_model = URLModel(**url_data)
    bill = Bill(**bill_data)
    # 合并url 和 bill
    dataset_data = {**url_data, **bill_data}
    dataset = DataSet(**dataset_data)
    dataset.insert()
    # res = URL(url_model).get_url()
    # print(res)
