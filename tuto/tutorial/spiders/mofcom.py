# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
import pytz
from tutorial.items import TutorialItem

class MofcomSpider(CrawlSpider):
    name = 'mofcom'
    allowed_domains = ['mofcom.gov.cn']
    start_urls = ["http://www.mofcom.gov.cn/article/ae/"]

    rules = (
        #Rule(LinkExtractor(allow=('category\.php', ), deny=('subsection\.php', ))),
        Rule(LinkExtractor(
            allow=(r'article/ae/[a-z]*?/2018[0-9]*?/[0-9]*?\.shtml', ),
            deny=(r'http://www.mofcom.gov.cn/article/ae/slfw/2018[0-9]*?/[0-9]*?\.shtml', r'http://www.mofcom.gov.cn/article/ae/ztfbh/2018[0-9]*?/[0-9]*?\.shtml')),
            callback='parse_content'),

        # Extract links matching 'item.php' and parse them with the spider's method parse_item
        Rule(LinkExtractor(allow=('/article/ae/ai', '/article/ae/ag')),
             follow=True),
        #Rule(LinkExtractor(allow=(r'http://www.mofcom.gov.cn/article/ae/ai/\?[0-9]')))
    )

    def parse_content(self, response):
        self.tz = pytz.timezone('Asia/Shanghai')


        # item['timestamp'] = datetime.datetime.now(tz=self.tz).strftime('%Y_%m_%d_%H_%M_%S')
        item = TutorialItem()
        item['link'] = response.url
        item['title'] = response.xpath('//html/body/div[@id="wrap"]/div[@class="MainList"]//h4/text()').extract_first()
        sel = response.xpath('//div[@id="zoom"]').xpath('string(.)').extract_first().strip()

        contents = response.xpath('//html/body/script').extract()[0].split('\n\t\t')

        item['desc'] = sel
        print item
        yield item
        pass
