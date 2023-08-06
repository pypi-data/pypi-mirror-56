# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html
import json
import os
import telnetlib
import threading
import time

import requests
from fake_useragent import UserAgent
from scrapy import signals
from xspider.utils.defaults import *


class MonetspiderSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    def __init__(self, crawler):
        self.crawler = crawler
        self.lock = threading.RLock()

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls(crawler)
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)

        return s

    def to_stop(self):
        if redis.sismember(STOP_KEY, self.uuid):
            return True
        return False

    def to_finish(self):
        if redis.sismember(FINISH_KEY, self.uuid):
            return True
        return False

    def stop(self, spider):
        redis.smove(RUN_KEY, STOPED_KEY, self.uuid)
        redis.srem(STOP_KEY, self.uuid)
        pass

    def finish(self, spider):
        redis.smove(RUN_KEY, FINISHED_KEY, self.uuid)
        redis.srem(FINISH_KEY, self.uuid)
        redis.delete(*redis.keys(self.name + "*"))

    def business(self,spider):
        if self.to_stop():
            # if stop ID
            # close spider ,stop ID to stoped ID
            self.lock.acquire()
            try:
                if self.to_stop():
                    self.crawler.engine.close_spider(spider, "stoped")
                    self.stop(spider)
            finally:
                self.lock.release()
        elif self.to_finish():
            # if finish Spider
            # close spider & clear spider,finish ID to finished ID
            self.lock.acquire()
            try:
                if self.to_finish():
                    self.crawler.engine.close_spider(spider)
                    self.finish(spider)
            finally:
                self.lock.release()
            pass

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.
        self.name = spider.name
        self.uuid = spider.uuid
        print("process_spider_input_" + spider.uuid)
        self.business(spider)
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

        # Should return either None or an iterable of Request, dict
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


class MonetspiderDownloaderMiddleware(object):
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


class RandomUserAgentMiddleware(object):
    def __init__(self, crawler):
        super(RandomUserAgentMiddleware, self).__init__()
        self.ua = UserAgent()

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)

    def process_request(self, request, spider):
        request.headers.setdefault('User-Agent', self.ua.random)


class RandomProxyMiddleware(object):

    def test_proxy(self, ip, port):
        try:
            # 49.77.211.163:4251
            telnetlib.Telnet(host=ip, port=port, timeout=6)
        except:
            redis.hset(ERROR_KEY, 'system_test_proxy_' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                       ip + ':' + port)
            return False
        else:
            print('该代理IP  有效')
            return True

    def get_from_pool(self):
        try:
            proxy = redis.srandmember(PROXY_KEY)
        except:
            return self.check_pool()
        else:
            if proxy is None:
                return self.check_pool()
            return proxy

    def get_proxy(self):
        return self.get_from_pool()

    def del_expire_proxy(self, proxy):
        redis.srem(PROXY_KEY, proxy)

    def del_request_proxy(self, request):
        if 'proxy' in request.meta:
            del request.meta['proxy']

    def set_proxy(self, request):
        proxy = self.get_proxy()
        if proxy:
            request.meta['proxy'] = 'http://' + proxy
            # request.meta['proxy'] =  proxy
        else:
            print("can not get proxy========")

    def process_request(self, request, spider):
        if 'proxy' in request.meta and request.meta['proxy'] is not None:
            print("request.meta['proxy']========" + request.meta['proxy'])
            return
        self.set_proxy(request)

    def process_exception(self, request, exception, spider):
        if 'proxy' not in request.meta:
            return None
        httpproxy = request.meta['proxy']
        try:
            proxy = httpproxy
            if str(httpproxy).startswith('http://'):
                proxy = httpproxy.replace('http://', '')
            elif str(httpproxy).startswith('https://'):
                proxy = httpproxy.replace('http://', '')

            ip, port = proxy.split(':')
            if self.test_proxy(ip, port):
                return None
            else:
                print(proxy + "-----")
                self.del_expire_proxy(proxy)
                self.set_proxy(request)
                return request
        except:
            self.del_request_proxy(request)
            return request

    def get_from_zhima(self):
        try:
            ret = requests.get(url=PROXY_API, timeout=PROXY_API_TIMEOUT)
            data = json.loads(ret.text)
            while data['code'] != 0:
                redis.hset(ERROR_KEY, 'system_get_from_zhima_' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                           data['code'] + ':' + data['msg'])
                time.sleep(2)
                ret = requests.get(url=PROXY_API)
                data = json.loads(ret.text)
            proxy = data['data'][0]['ip'] + ':' + str(data['data'][0]['port'])
            self.save_to_pool(proxy)

        except Exception as e:
            now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            redis.hset(ERROR_KEY, 'system_proxy_' + now, "error")
            return None
        else:
            return proxy

    def save_to_pool(self, proxy):
        redis.sadd(PROXY_KEY, proxy)

    def check_pool(self):
        while (redis.scard(PROXY_KEY) < PROXY_NUM):
            proxy = self.get_from_zhima()
            if proxy is None:
                time.sleep(2)
            else:
                self.save_to_pool(proxy)
        return redis.srandmember(PROXY_KEY)
