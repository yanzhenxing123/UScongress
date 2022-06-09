"""
@Author: yanzx
@Date: 2022/5/26 23:17
@Description: 
"""
from pydantic import BaseModel, Field
from typing import List
from config import db

conn = db.MysqlConn.get_conn()


class URLModel(BaseModel):
    """
    URL模型类
    """

    congressGroup: List[int] = Field(None, description="{1973-2022, 1951-1972, 1799-1811, 1813-1873}, [1, 2, 3]")
    congress: List[int] = Field(None, description="国会", alias='congresses[]')
    legislationNumbers: str = Field(None, description="eg: hr5")
    restrictionType: str = Field('field', description="restrictionType")
    restrictionFields: List[str] = Field(['allBillTitles', 'summary'], description="restrictionType", alias='restrictionFields[]')
    summaryField: str = Field('billSummary')
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
        url_dict = self.url_model.dict()
        for key in url_dict.keys():
            value = url_dict.get(key)
            if not value:
                continue
            elif isinstance(value, List):
                key = key + "[]"
                for item in value:
                    res_li.append(key + "=" + str(item))
            else:
                res_li.append(key + "=" + str(value))
        res_str = "&".join(res_li)
        return self.base_url + res_str


class Bill(BaseModel):
    bill_id: int = Field(None, description='')
    type: str = Field(None, description='')
    tracker: str = Field(None, description='')
    heading: str = Field(None, description='')
    bill_url: str = Field(None, description='')
    title: str = Field(None, description='')
    sponsor: str = Field(None, description='', alias='Sponsor')
    sponsor_url: str = Field(None, description='', alias='Sponsor_url')
    cosponsors: int = Field(None, description='', alias='Cosponsors')
    latest_action: str = Field(None, description='', alias='Latest Action')

    def insert(self, table: str = 'bill'):
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
    data = {
        'congress_group': 1,
        'congress': None,
        'member': None,
        'legislationNumbers': None,
        'enterTerms': 'health care',
        'actionTerms': 8000,
        'satellite': None,
    }
    url_model = URLModel(**data)
    res = URL(url_model).get_url()
    print(res)
