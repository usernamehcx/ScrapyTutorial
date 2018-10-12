# -*- coding: utf-8 -*-
import scrapy
import time
import datetime
import pytz
from scrapy.spiders import CrawlSpider,Rule
from scrapy.linkextractors import LinkExtractor
from scrapy_splash.request import SplashRequest, SplashFormRequest
from zhijian.items import ZhijianItem


class ZhijianSpiderSpider(scrapy.Spider):
    name = 'zhijian'
    allowed_domains = ['samr.aqsiq.gov.cn']
    start_urls = ['http://samr.aqsiq.gov.cn/xxgk_13386/ywxx/cpzljd/']

    def __init__(self):
        self.tz = pytz.timezone( 'Asia/Shanghai' )
        self.url =''


    def parse(self, response):
        self.url = response.url
        #定位到iframe标签，拼接成URL
        iframe = response.selector.xpath('//iframe/@src')[0].extract()
        url = response.url + iframe

        splash_args = {"lua_source": """ 
                    --splash.response_body_enabled = true 
                    splash.private_mode_enabled = false 
                    splash:set_user_agent('Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36') \
                    assert(splash:go('%s')) 
                    splash:wait(3) 
                    return {html = splash:html()} 
                    """ % (url)}

        #由于上面URL消息动态加载，需要yield SplashRequest
        yield SplashRequest(url,endpoint='run',args=splash_args,callback=self.parse_iframe)
        pass

    def parse_iframe(self,response):
#        now = datetime.datetime.now(self.tz)
        now = datetime.date(2018,4,4)

        #获取所有的消息所在节点的集合，并遍历它
        trs = response.xpath('//body/table/tbody/tr/td[@class="border2"]/table/tbody/tr')

        count = 0
        for tr in trs:
            #定位到每一条消息所在节点
            tds = tr.xpath('.//td')
            #读取每一条信息的URL
            href = tds[1].xpath('.//a/@href').extract_first()
            #读取x消息发布的时间，并格式化成datetime
            time = tds[2].xpath('string(.)').extract_first()
            format_time = datetime.datetime.strptime(time,"%Y-%m-%d")

            #比较时间信息，在年份，月份相同的情况下，日期相差小于1，则跟进这个URL，继续进行爬取这个URL的内容
            if ( (now.year == format_time.year) and (now.month == format_time.month ) and (now.day-format_time.day) <= 1 ):
                count = count + 1
                url = self.url + href
                print str(now.day)
                print url
                yield scrapy.Request(url,callback=self.parse_one,meta={'time': time})
            else:
                break


        #count用于计数，因为没给table都会给出22条消息，如果这22条信息都是昨天发生的，那么我们继续跟进下一页
        if (count == 22) :
            a_list = response.xpath('//td[@class="border2"]/div/a')
            for a in a_list:

                href = a.xpath('./@href').extract_first()
                page = a.xpath('string(.)').extract_first()
                if (page == u'下一页'):

                    #拼接成下一页的链接URL
                    url = self.url + href

                    splash_args = {"lua_source": """ 
                    --splash.response_body_enabled = true 
                    splash.private_mode_enabled = false 
                    splash:set_user_agent('Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36') \
                    assert(splash:go('%s')) 
                    splash:wait(3) 
                    return {html = splash:html()} 
                    """ % (url)}

                    #由于下一页的列表也是动态加载的，我们需要用SplashRequest
                    yield SplashRequest(url,endpoint='run',args=splash_args,callback=self.parse_iframe)


    def parse_one(self,response):

        item = ZhijianItem()
        item['title'] = response.xpath('//div[@id="reference"]//h1').xpath('string(.)').extract_first()
        item['time'] = response.meta['time']
        item['content'] = response.xpath('//td[@class="border"]//div[@class="zh"]/div').xpath('string(.)').extract_first()
        yield item










