# -*- coding: utf-8 -*-
import json
import time
from collections import defaultdict
from twisted.internet import reactor
from scrapy import signals
from scrapy.exceptions import NotConfigured
from xspider.utils.defaults import redis, spider_clear, spider_stop, spider_finish, RUN_KEY, FINISHED_KEY, FINISH_KEY, \
    NAME
import logging

logger = logging.getLogger(__name__)


class CloseSpider(object):

    def __init__(self, crawler):
        self.crawler = crawler
        crawler.signals.connect(self.start_monit, signal=signals.spider_opened)
        # self.url = "http://localhost:8063/ringspiderapi/task/v1/python/callback"
        # 回掉接口
        self.url = redis.get("monet:business:callback")
        self.idle_number = 3
        self.idle_count=0
        self.idle_list = []

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)

    def error_count(self, failure, response, spider):
        self.counter['errorcount'] += 1
        if self.counter['errorcount'] == self.close_on['errorcount']:
            self.crawler.engine.close_spider(spider, 'closespider_errorcount')

    def page_count(self, response, request, spider):
        self.counter['pagecount'] += 1
        if self.counter['pagecount'] == self.close_on['pagecount']:
            self.crawler.engine.close_spider(spider, 'closespider_pagecount')

    def spider_opened(self, spider):
        self.task = reactor.callLater(self.close_on['timeout'], \
                                      self.crawler.engine.close_spider, spider, \
                                      reason='closespider_timeout')

    def start_monit(self, spider):
        self.close_on = {
            'timeout': spider.settings['taskdict'].get('CLOSESPIDER_TIMEOUT'),
            'itemcount': spider.settings['taskdict'].get('CLOSESPIDER_ITEMCOUNT'),
            'pagecount': spider.settings['taskdict'].get('CLOSESPIDER_PAGECOUNT'),
            'errorcount': spider.settings['taskdict'].get('CLOSESPIDER_ERRORCOUNT'),
        }
        if not any(self.close_on.values()):
            raise NotConfigured

        self.counter = defaultdict(int)

        if self.close_on.get('errorcount'):
            self.crawler.signals.connect(self.error_count, signal=signals.spider_error)
        if self.close_on.get('pagecount'):
            self.crawler.signals.connect(self.page_count, signal=signals.response_received)
        if self.close_on.get('timeout'):
            self.crawler.signals.connect(self.spider_opened, signal=signals.spider_opened)

        self.crawler.signals.connect(self.item_scraped, signal=signals.item_scraped)
        self.crawler.signals.connect(self.spider_closed, signal=signals.spider_closed)
        self.crawler.signals.connect(self.spider_idle, signal=signals.spider_idle)
        pass

    def item_scraped(self, item, spider):
        self.counter['itemcount'] += 1
        if int(self.close_on['itemcount']) > 0 and int(self.counter['itemcount']) == int(self.close_on['itemcount']):
            self.crawler.engine.close_spider(spider)

    def spider_closed(self, spider, reason):
        task = getattr(self, 'task', False)
        if task and task.active():
            task.cancel()

        if reason is "finished" or reason is "cancelled":
            self.spider_clear(spider)
            self.finish_callback(spider)
        elif reason is "stoped":
            self.stop_callback(spider)
        elif reason is "shutdown":
            self.stop_callback(spider)
            pass
        print("zzz reason:" + reason)

    def spider_clear(self, spider):
        redis.smove(RUN_KEY, FINISHED_KEY, spider.uuid)
        redis.srem(FINISH_KEY, spider.uuid)
        for i in redis.keys(NAME + ":" + spider.uuid + ":*"):
            redis.delete(i)

    def finish_callback(self, spider):
        import requests
        try:
            headers = {'Content-Type': 'application/json'}
            jsonparam = json.dumps({'uuid': spider.uuid, 'opt': 'FINISH'})
            response = requests.post(self.url, headers=headers, data=jsonparam)
            if response.status_code is 200:
                print("调用成功")
                pass
            else:
                print("调用失败")
                pass
        except Exception as e:
            print(e)

        pass

    def stop_callback(self, spider):
        import requests
        try:
            headers = {'Content-Type': 'application/json'}
            jsonparam = json.dumps({'uuid': spider.uuid, 'opt': 'STOP'})
            response = requests.post(self.url, headers=headers, data=jsonparam)
            if response.status_code is 200:
                print("调用成功")
                pass
            else:
                print("调用失败")
                pass
        except Exception as e:
            print(e)

    def spider_idle(self, spider):
        self.idle_count += 1
        self.idle_list.append(time.time())
        idle_list_len = len(self.idle_list)
        if idle_list_len > 2 and self.idle_list[-1] - self.idle_list[-2] > 6:
            self.idle_list = [self.idle_list[-1]]

        elif idle_list_len > self.idle_number:
            self.crawler.engine.close_spider(spider)
