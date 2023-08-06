# -*- coding: utf-8 -*-

import time
from multiprocessing import Process, freeze_support
from ringspider.xspider.spiders.XspiderSpider import *
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from ringspider.xspider.config import TaskConfig, SpiderConfig


class MTSpiderServer:

    def __init__(self):
        self.redisMonit = True
        self.crawlers = []
        self.settings = get_project_settings()

    def run(self, uuid):
        param = redis.hget(PARAM_KEY, uuid)
        taskConfig = TaskConfig(param)
        try:
            self.settings['taskdict'] = taskConfig.dict
        except Exception as e:
            print(e)
        crawler = CrawlerProcess(self.settings)
        crawler.crawl(XspiderSpider, uuid=uuid)
        crawler.start()

    def start(self):
        while self.redisMonit:
            uuid = redis.spop(WAIT_KEY)
            if uuid is None:
                print("sleep....")
                time.sleep(1)
                continue
            # TODO 合法性 一致性 检查
            xmlstr = redis.hget(XML_KEY, uuid)
            if xmlstr is None:
                redis.hset(ERROR_KEY, uuid, 'xml is none')
                continue

            param = redis.hget(PARAM_KEY, uuid)
            xspider = Xspider(xmlstr)
            taskConfig = TaskConfig(param)
            taskConfig.dict['taskId'] = uuid
            spiderConfig = SpiderConfig(xspider, taskConfig)

            if spiderConfig:
                try:
                    p = Process(target=self.run, args=(uuid,))
                    p.start()

                    redis.sadd(RUN_KEY, uuid)
                except Exception as e:
                    print(e)
                    redis.hset(ERROR_KEY, uuid, 'start fail')


def main():
    freeze_support()
    manageSpider = MTSpiderServer()
    manageSpider.start()


if __name__ == '__main__':
    main()
