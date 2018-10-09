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
