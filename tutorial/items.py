# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html


import scrapy

class TutorialItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    link = scrapy.Field()
    desc = scrapy.Field()
    pass

class ScrapyBaiduItem(scrapy.Item):
    # define the fields for your item here like:
    # name = Scrapy.Field()
    url = scrapy.Field()
    title = scrapy.Field()
    abstract = scrapy.Field()
    keyword = scrapy.Field()
    #html = ''
    time = scrapy.Field()
    create_time = scrapy.Field()
    pass
