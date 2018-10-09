# -*-coding:utf-8-*-
import pytz
import redis
import scrapy
from scrapy.spiders import Spider
#import pyreBloom
from tutorial.items import ScrapyBaiduItem
import time
import datetime
#import MySQLdb
import sys
import os
reload(sys)
sys.setdefaultencoding('utf-8')

class BaiduSpider(Spider):
    name = 'baidu'
    def __init__(self, keyword=u'研考', page=1, *args, **kwargs):
        super(BaiduSpider, self).__init__(*args, **kwargs)
        if isinstance(keyword,str):
            try:
                self.keyword = unicode(keyword)
            except:
                self.keyword = keyword.decode('gb2312')
            # self.keyword = keyword
            print self.keyword
        else:
            self.keyword = keyword
        self.page = page
        self.tz = pytz.timezone('Asia/Shanghai')

    def start_requests(self):
        # keywords = ['提供', '发现',  '研考', '硕士考试', '硕士生考试', '成考', '成人高考', '自考', '自学考试']


        d = datetime.datetime.now(self.tz)
        d1 = d.replace( hour=0, minute=0, second=0, microsecond=0 )
        d2 = d1 - datetime.timedelta( days=3 )
        t1 = int( time.mktime( d1.timetuple() ) )
        t2 = int( time.mktime( d2.timetuple() ) )
        url_p1 = 'https://www.baidu.com/s?wd='
        url_p2 = '&pn='
        url_p3 = '&gpc=stf%3D' + str( t2 ) + '%2C' + str( t1 ) + '|stftype%3D2'

        url = url_p1 + self.keyword + url_p2 + str(self.page) + url_p3

        yield scrapy.Request( url=url, dont_filter=True, callback=self.parse,
                                              meta={'keyword': self.keyword} )


    def parse(self, response):
        # print response.text
        keyword = response.meta['keyword']
        results = response.xpath('//div[@class="result c-container "]')
        #print results
        time = datetime.datetime.now(self.tz)

        for res in results:
            #print res.extract()
            url = res.xpath('.//h3[contains(@class,"t")]/a/@href').extract_first()
            # print keyword,url
            bfdata = str(keyword) + str(url)


            item = ScrapyBaiduItem()
            item['url'] = url
            print url
            item['title'] = res.xpath('.//h3[contains(@class,"t")]/a').xpath('string(.)').extract_first()
            timestr = res.xpath( './/span[contains(@class," newTimeFactor_before_abs m")]' ).xpath(
                'string(.)' ).extract_first()
            # print timestr
            if timestr == None:
                item['time'] = time.strftime( '%Y_%m_%d_%H_%M_%S' )
            else:
                if str( timestr ).find( '天前' ) != -1:
                    time_num = int( timestr[:str( timestr ).find( '天前' )] )
                    delta = datetime.timedelta( days=time_num )
                    new_time = time - delta
                    item['time'] = new_time.strftime( '%Y_%m_%d_%H_%M_%S' )
                elif str( timestr ).find( '小时前' ) != -1:
                    time_num = int( timestr[:str( timestr ).find( '小时前' )] )
                    delta = datetime.timedelta( hours=time_num )
                    new_time = time - delta
                    item['time'] = new_time.strftime( '%Y_%m_%d_%H_%M_%S' )
                elif str( timestr ).find( '分钟前' ) != -1:
                    time_num = int( timestr[:str( timestr ).find( '分钟前' )] )
                    delta = datetime.timedelta( minutes=time_num )
                    new_time = time - delta
                    item['time'] = new_time.strftime( '%Y_%m_%d_%H_%M_%S' )
                elif str( timestr ).find( '秒钟前' ) != -1:
                    time_num = int( timestr[:str( timestr ).find( '秒钟前' )] )
                    delta = datetime.timedelta( seconds=time_num )
                    new_time = time - delta
                    item['time'] = new_time.strftime( '%Y_%m_%d_%H_%M_%S' )
            #print title
            abstract = res.xpath('.//div[contains(@class,"c-abstract")]').xpath('string(.)').extract_first()
            if abstract == None:
                #print res.extract()
                abstract = res.xpath('.//div[@class="c-span18 c-span-last"]/font/p').xpath('string(.)').extract()
                abstract = ' '.join(abstract)
                    #print abstract
                #print abstract
            s = abstract.find( '-' )
            if s > 0:
                abstract = abstract[s + 2:]
            item['abstract'] = abstract
            item['keyword'] = unicode(keyword)
            item['create_time'] = time.strftime('%Y_%m_%d_%H_%M_%S')
            yield item
