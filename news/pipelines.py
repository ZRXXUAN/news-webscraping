# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
import redis
from news.tools.general.standardize_turn_list_to_string import list_to_string
from news.tools.general.save_group_api import save


class SavePipeline(object):
    def __init__(self, mongo_host, mongo_port, mongo_db, redis_host, redis_port, redis_password, redis_key, save_url):  # save_url是存储组的api
        self.mongo_host = mongo_host
        self.mongo_port = mongo_port
        self.mongo_db = mongo_db
        self.client_mongo = None
        self.db = None
        self.redis_host = redis_host
        self.redis_port = redis_port
        self.redis_password = redis_password
        self.redis_key = redis_key
        self.client_redis = None
        self.save_url = save_url  # save_url是存储组的api

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_host=crawler.settings.get('MONGO_HOST'),
            mongo_port=crawler.settings.get('MONGO_PORT'),
            mongo_db=crawler.settings.get('MONGO_DB'),
            redis_host=crawler.settings.get('REDIS_HOST'),
            redis_port=crawler.settings.get('REDIS_PORT'),
            redis_password=crawler.settings.get('REDIS_PASSWORD'),
            redis_key=crawler.settings.get('REDIS_KEY'),
            save_url=crawler.settings.get('SAVE_URL'),
        )

    def open_spider(self, spider):
        self.client_mongo = pymongo.MongoClient(host=self.mongo_host)  # 不填参数默认为localhost:27017，docker版见下面的注释
        self.db = self.client_mongo[self.mongo_db]
        self.client_redis = redis.Redis(host=self.redis_host)  # 这是docker版，采用自建桥接网络，可使用容器名，有DNS解析

    def process_item(self, item, spider):
        name = item.__class__.__name__
        if self.client_redis.sismember(self.redis_key, item['url']):
            return item
        else:
            self.client_redis.sadd(self.redis_key, item['url'])
            self.db[name].insert(dict(item))
            # save(item, self.save_url)
            return item

    def close_spider(self, spider):
        self.client_mongo.close()


class StandardizationPipeline(object):
    def process_item(self, item, spider):

        item['title'] = list_to_string(item['title'])
        self.string = list_to_string(item['source'])
        item['source'] = self.string
        item['source_url'] = list_to_string(item['source_url'])
        if item['content']:
            if isinstance(item['content'], list):
                item['content'] = "".join(item['content'])
        else:
            item['content'] = ''

        # attribute因为通过tools中函数得到，本身就是字符串
        # url, date也都是字符串
        return item
