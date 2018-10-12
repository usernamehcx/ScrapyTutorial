# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


import json
import codecs
from collections import OrderedDict

class TutorialPipeline(object):
    def __init__(self):
        self.filename = 'mofcom.txt'
    def process_item(self, item, spider):
        file = codecs.open(self.filename, 'a', encoding='utf-8')
        line = json.dumps(OrderedDict(item), ensure_ascii=False, sort_keys=False) + "\n"
        file.write(line)
        file.close()
        return item

import pymongo

class MongoPipeline(object):

    collection_name = 'baidu'

    def __init__(self, mongo_host,mongo_port, mongo_db):
        self.mongo_host = mongo_host
        self.mongo_port = mongo_port
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_host=crawler.settings.get('MONGODB_HOST'),
            mongo_port=crawler.settings.get('MONGODB_PORT'),
            mongo_db=crawler.settings.get('MONGODB_DBNAME')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_host,self.mongo_port)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        self.db[self.collection_name].insert(dict(item))
        return item
