# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals

import scrapy
import requests
from scrapy import signals, log
import base64
from weibo.settings import PROXY_SERVICE_ADDRESS
import random

class WeiboSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class WeiboDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class ProxyMiddleware(object):

    def __init__(self, ip=''):
        self.ip = ip
    # def __init__(self):
        # self.proxy = DEFAULT_PROXY
        # self.proxy_use = 0
        # self.max_use = int(PROXY_MAX_USE)
        # self.proxy = self.update_proxy()

    # def update_proxy(self):
    #     return "bh21.84684.net:21026"
        # service_address = PROXY_SERVICE_ADDRESS+'get/'
        # # print service_address
        # try:
        #     response = requests.get(service_address, timeout=5)
        #     # print response.status_code
        #     if response.status_code == 200:
        #         return response.text
        #     return self.proxy
        # except:
        #     print " failed get service_address"
        #     return self.proxy

    def process_request(self, request, spider):
        service_address = PROXY_SERVICE_ADDRESS
        # print service_address
        try:
            response = requests.get(service_address, timeout=10)
            # print response.status_code
            if response.status_code == 200:
                proxy = response.text
                request.meta['proxy'] = 'http://' + proxy
                print request.meta['proxy']
        except:
            # request.meta['proxy'] = 'http://127.0.0.1:9743'
            print " failed get new service_address"

        # proxy_user_pass = "dailaoshi:D9xvyfrgPwqBx39u"
        # encoded_user_pass = base64.encodestring( proxy_user_pass )
        # request.headers['Proxy-Authorization'] = 'Basic ' + encoded_user_pass

        # if request.meta.get('change_proxy', False):
        #     self.proxy = self.update_proxy()
        #     msg = 'ProxyMiddleware: Change proxy to:' + self.proxy
        #     log.msg(msg, level=log.INFO)
        #     request.meta['change_proxy'] = False
        # request.meta['proxy'] = 'http://'+self.proxy
        # print request.meta['proxy']
        # self.proxy_use += 1
        # if self.proxy_use > self.max_use:
        #     self.proxy_use = 0
        #     self.proxy = self.update_proxy()
        #     msg = 'Change proxy to:' + self.proxy
        #     log.msg(msg, level=log.INFO)
        return None
        # request.meta['proxy'] = 'http://110.206.127.136:9797'
