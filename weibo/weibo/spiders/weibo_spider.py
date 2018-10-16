# -*- coding: utf-8 -*-

from scrapy.spiders import Spider
from items import WeiboItem
import scrapy
import pytz
import json
import datetime
import time
import re

class WeiboSpider(Spider):
    name = 'weibo'

    def __init__(self, keyword=u'南京', page=3, *args, **kwargs):
        super(WeiboSpider, self).__init__(*args, **kwargs)
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

    # def start_requests(self):
    #     username = '18169209977'
    #     url = 'http://login.sina.com.cn/sso/prelogin.php?entry=miniblog&callback=sinaSSOController.preloginCallBack&user=%s&client=ssologin.js(v1.3.14)&_=%s'  % \
    #         (username, str(time.time()).replace('.', ''))
    #     print url
    #     return [scrapy.Request(url=url, method='get', callback=self.post_message,meta={'cookiejar' : 1} )]
    #
    #
    # def post_message(self, response):
    #
    #     serverdata = re.findall(r'"retcode":0,"servertime":(.*?),', response.body, re.I)
    #     print serverdata
    #     servertime = serverdata[0]
    #     print servertime
    #
    #     serverdata = re.findall('"nonce":"(.*?)"', response.body, re.I)
    #     print serverdata
    #     nonce = serverdata[0]
    #     print nonce
    #     formdata = {"entry" : 'miniblog',
    #                 "gateway" : '1',
    #                 "from" : "",
    #                 "savestate" : '7',
    #                 "useticket" : '1',
    #                 "ssosimplelogin" : '1',
    #                 "username" : '18169209977',
    #                 "service" : 'miniblog',
    #                 "servertime" : servertime,
    #                 "nonce" : nonce,
    #                 "pwencode" : 'wsse',
    #                 "password" : 'hecheng123',
    #                 "encoding" : 'utf-8',
    #                 "url" : 'http://weibo.com/ajaxlogin.php?framelogin=1&callback=parent.sinaSSOController.feedBackUrlCallBack',
    #                 "returntype" : 'META'}
    #
    #     return [scrapy.FormRequest(url = 'http://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.3.14)',
    #                                meta = {'cookiejar' : response.meta['cookiejar']},
    #                             formdata = formdata,callback=self.afterlogin) ]



    def start_requests(self):

        # cookies = { "YF-Ugrow-G0":"57484c7c1ded49566c905773d5d00f82",
        #             "login_sid_t":"6ca8ea9621860078d63358931b537fa1",
        #             "cross_origin_proto":"SSL",
        #             "YF-V5-G0":"590253f9bb559fcb4f19c58020522401",
        #             "_s_tentry":"passport.weibo.com",
        #             "Apache":"1932791264390.1345.1539329867676",
        #             "SINAGLOBAL":"1932791264390.1345.1539329867676",
        #             "ULV":"1539329867684:1:1:1:1932791264390.1345.1539329867676:",
        #             "WBStorage":"e8781eb7dee3fd7f|undefined",
        #             "wb_view_log":"1440*9002",
        #             "UOR":",,www.baidu.com",
        #             "SUBP":"0033WrSXqPxfM725Ws9jqgMF55529P9D9W5DNKRT0qumQKo-Z50HRAr_5JpX5K2hUgL.Fo-0eoMNeh50Shn2dJLoI79VIrHQqNnt",
        #             "ALF":"1571212859",
        #             "SSOLoginState":"1539676860",
        #             "SCF":"AmHun9sz-Io-fLCss7-KTP1j6DdW8VXmTga-w8C3dkAWGHT_RrmDLI9BKE6DNGHo1r3fS7CruP2tfWwv0BXbA_Q.",
        #             "SUB":"_2A252weruDeRhGeNN6VUW8C7PzzSIHXVVt1smrDV8PUNbmtBeLRTVkW9NSdFig5QZV9sWNTTHry4pI8ZbW2EGjEFv",
        #             "SUHB":"0OMUdt6daCy9_g",
        #             "un":"***********"
        #             }

        cookies = {}
        url_p1 = 'https://s.weibo.com/weibo?q='
        url_p2 = '&wvr=6&b=1&Refer=SWeibo_box&page='

        ip_list = [
            "122.194.214.32:22050",
            "114.234.200.12:57214",
        ]
        url = url_p1 + self.keyword + url_p2 + str(self.page)
        # url = url_p1 + keyword + url_p2 + keyword + url_p3 + keyword + url_p4 + str(self.page)
        yield scrapy.Request(url=url, callback=self.parse_search, dont_filter=True,meta={'keyword':self.keyword},cookies=cookies)

    def parse_search(self,response):

        item = WeiboItem()
        results=response.xpath('//div[@class="card-wrap"]')

        from scrapy.shell import inspect_response
        inspect_response(response,self)

        for re in results:
            contents = re.xpath('./div/div/div[@class="content"]/p[@class="txt"]')
            if(len(contents) > 1):
                item['content'] = contents[1].xpath('string(.)').extract_first()
            elif (len(contents) == 1):
                item['content'] = contents[0].xpath('string(.)').extract_first()

            else:
                item['content']=''

            item['time'] = re.xpath('./div/div/div[@class="content"]/p[@class="from"]/a').xpath('string(.)').extract_first()
            item['name'] = re.xpath('./div/div/div[@class="content"]/div[@class="info"]//a[@class="name"]/@nick-name').extract_first()

            yield item


