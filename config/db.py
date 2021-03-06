import random

import pymongo
import redis

from config import config
from typing import List
from confluent_kafka import Consumer as KafkaConsumer
import pymysql
from loguru import logger


class Mongo(object):
    def __init__(self, url):
        self.url = url
        self.conn = pymongo.MongoClient(url)

    def __enter__(self):
        return self.get_session()

    def get_session(self):
        return self.conn

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.close()


class Consumer(object):
    def __init__(self, Topics: List[str]):
        self.addr = ",".join(config.Kafka['Addr'])
        # self.group_id = config.Kafka['GroupId']
        self.group_id = str(random.randint(0, 1000000))
        self.offset = config.Kafka['Offset']
        self.topics = Topics
        self.consumer = KafkaConsumer(
            {
                'bootstrap.servers': self.addr,
                'group.id': self.group_id,
                'auto.offset.reset': self.offset,
            }
        )

    def consume(self, timeout):
        while True:
            message = self.consumer.poll(timeout)
            if message is None:
                continue
            if message.error():
                print("Consumer error: {}".format(message.error()))
                continue
            yield message
        self.consumer.close()

    def confluent_consumer(self, timeout: float):
        # 订阅所有的topic
        self.consumer.subscribe(self.topics)
        yield from self.consume(timeout)


class MysqlConn:
    user = config.Mysql['user']
    pwd = config.Mysql['pwd']
    host = config.Mysql['host']
    port = config.Mysql['port']
    database = config.Mysql['database']

    @classmethod
    def get_conn(cls):
        try:
            return pymysql.connect(
                user=cls.user,
                password=cls.pwd,
                host=cls.host,
                port=cls.port,
                database=cls.database,
            )
        except Exception as e:
            logger.error(e)
            return None


class Redis:
    pwd = config.Redis['pwd']
    host = config.Redis['host']
    port = config.Redis['port']
    database = config.Redis['database']

    pool = redis.ConnectionPool(host=host,
                                port=port,
                                password=pwd,
                                db=database,
                                decode_responses=True
                                )  # host是redis主机，需要redis服务端和客户端都起着 redis默认端口是6379

    @classmethod
    def get_conn(cls):
        try:
            redis_conn = redis.Redis(connection_pool=cls.pool)
            return redis_conn
        except Exception as e:
            logger.error(e)
            return None


if __name__ == '__main__':
    conn = Redis.get_conn()
