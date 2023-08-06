# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import datetime

from pymongo import MongoClient
import pymysql
import json
from scrapy.pipelines.files import FilesPipeline
from ringspider.xspider.utils.defaults import redis
import threading


class DefaultValuePipeline(object):
    def __init__(self):
        pass

    @classmethod
    def from_crawler(cls, crawler):
        return cls()

    def open_spider(self, spider):
        self.defaultItem = Item()
        for datacol in spider.xspider.datacols:
            if datacol.defaultValue and datacol.defaultValue.__str__().__len__() > 0:
                self.defaultItem.fields[datacol.name] = Field()
                self.defaultItem[datacol.name] = datacol.defaultValue

    def process_item(self, item, spider):
        for key in item.keys():
            if item[key] is None and self.defaultItem.__contains__(key):
                item[key] = self.defaultItem[key]
        return item

    def close_spider(self, spider):
        pass


class SystemValuePipeline(object):
    def __init__(self):
        pass

    @classmethod
    def from_crawler(cls, crawler):
        return cls()

    def open_spider(self, spider):
        pass

    def process_item(self, item, spider):
        item.fields['timestamp'] = Field()
        item["timestamp"] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        # if item.__contains__('URL'):
        #     item.fields['download_fileurl'] = Field()
        #     item["download_fileurl"] = item['URL']
        item.fields['missing_data'] = Field()
        item["missing_data"] = "1" if spider.hasNoneCol(item) else "0"
        return item

    def close_spider(self, spider):
        pass


class MongoPipeline(object):
    def __init__(self, mongo_host, mongo_port, mongo_db):
        self.mongo_host = mongo_host
        self.mong_port = mongo_port
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_host=crawler.settings.get('MONGO_HOST'),
            mongo_port=crawler.settings.get('MONGO_PORT'),
            mongo_db=crawler.settings.get('MONGO_DB')
        )

    def open_spider(self, spider):
        self.client = MongoClient(host=self.mongo_host, port=self.mong_port)
        self.db = self.client[self.mongo_db]

    def process_item(self, item, spider):
        self.db[spider.uuid].insert(dict(item))
        return item

    def close_spider(self, spider):
        self.client.close()


class MysqlPipeline():
    def __init__(self, host, database, user, password, port):
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.port = port
        print("host mysql ======.text")

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            host=crawler.settings.get('MYSQL_HOST'),
            database=crawler.settings.get('MYSQL_DATABASE'),
            user=crawler.settings.get('MYSQL_USER'),
            password=crawler.settings.get('MYSQL_PASSWORD'),
            port=crawler.settings.get('MYSQL_PORT'),
        )

    def open_spider(self, spider):
        self.db = pymysql.connect(self.host, self.user, self.password, self.database, charset='utf8', port=self.port)
        # self.db.ping(reconnect=True)
        # self.cursor = self.db.cursor()
        # createsql = ""
        # createsql += 'CREATE TABLE if not exists `news_' + spider.uuid + '` ('
        # createsql += "`id` int(11) NOT NULL AUTO_INCREMENT,"
        # createsql += "`title` varchar(200) DEFAULT NULL,"
        # createsql += "`pub_time` varchar(200) DEFAULT NULL,"
        # createsql += "`media` varchar(200) DEFAULT NULL,"
        # createsql += "`content` longtext,"
        # createsql += "`URL` varchar(200) NOT NULL,"
        # createsql += "`TIMESTAMP` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,"
        # createsql += "`missing_data` varchar(1) NOT NULL DEFAULT '0',"
        # createsql += "PRIMARY KEY (`id`)"
        # createsql += ") ENGINE=InnoDB DEFAULT CHARSET=utf8;"
        # self.cursor.execute(createsql)
        # self.db.commit()

    def close_spider(self, spider):
        self.db.close()

    def process_item(self, item, spider):
        data = dict(item)
        keys = ', '.join(data.keys())
        values = ', '.join(['%s'] * len(data))
        table = item.table + "_" + spider.uuid
        sql = 'insert into %s (%s) values (%s)' % (table, keys, values)
        try:
            self.db.ping(reconnect=True)
            self.cursor.execute(sql, tuple(data.values()))
            self.db.commit()

        except Exception as e:
            print(e)
        finally:
            self.db.rollback()
            # spider.crawler.stats.inc_value("collectNum")
        # raise DropItem("Missing price in %s" % item)
        # spider.crawler.engine.close_spider(self, reason='finished')
        return item


from scrapy import Request, Item, Field
from scrapy.pipelines.images import ImagesPipeline


class ImagePipeline(ImagesPipeline):
    def file_path(self, request, response=None, info=None):
        url = request.url
        file_name = url.split('/')[-1]
        return file_name

    def item_completed(self, results, item, info):
        if item.get('download_imgurl'):
            item.__delitem__("download_imgurl")
        image_paths = [x['path'] for ok, x in results if ok]
        # if not image_paths:
        #     raise DropItem('Image Downloaded Failed')
        return item

    def get_media_requests(self, item, info):
        if item.get('download_imgurl'):
            yield Request(item['download_imgurl'])


class ZFilePipeline(FilesPipeline):
    def file_path(self, request, response=None, info=None):
        url = request.url
        file_name = url.split('/')[-1]
        return info.spider.uuid + '/' + file_name

    def item_completed(self, results, item, info):
        if item.get('download_fileurl'):
            item.__delitem__("download_fileurl")
        image_paths = [x['path'] for ok, x in results if ok]
        # if not image_paths:
        #     raise DropItem('files Downloaded Failed')
        return item

    def get_media_requests(self, item, info):
        if item.get('download_fileurl'):
            yield Request(item['download_fileurl'])


class RedisPipeline():
    def __init__(self):
        self.name = "monet:testdata:"
        pass

    @classmethod
    def from_crawler(cls, crawler):
        return cls()

    def open_spider(self, spider):
        self.redis = redis
        self.redis.delete(self.name + spider.uuid)

    def close_spider(self, spider):

        pass

    def process_item(self, item, spider):
        try:
            if spider.crawler.stats.get_value("collectNum") <= spider.settings['taskdict'].get('CLOSESPIDER_ITEMCOUNT'):
                self.redis.sadd(self.name + spider.uuid, json.dumps(dict(item), ensure_ascii=False))
        except Exception as e:
            print(e)
        finally:
            pass
        return item


class RingspiderPipeline:

    def __init__(self, host, database, user, password, port):
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.port = port
        self.name = "monet:business:testdata:"
        self.lock = threading.RLock()
        print("host mysql ======.text")

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            host=crawler.settings.get('MYSQL_HOST'),
            database=crawler.settings.get('MYSQL_DATABASE'),
            user=crawler.settings.get('MYSQL_USER'),
            password=crawler.settings.get('MYSQL_PASSWORD'),
            port=crawler.settings.get('MYSQL_PORT'),
        )

    def open_spider(self, spider):
        spider.crawler.stats.set_value("collectNum", 0)
        self.redis = redis
        if str(spider.uuid).startswith("TEST"):
            self.redis.delete(self.name + spider.uuid)
            pass
        else:
            self.db = pymysql.connect(self.host, self.user, self.password, self.database, charset='utf8',
                                      port=self.port)
            pass

    def close_spider(self, spider):
        if str(spider.uuid).startswith("TEST"):
            pass
        else:
            self.db.close()
        pass

    def business(self, uuid):
        self.redis.incr("monet:business:count:" + uuid)
        userId = str(self.redis.hget("monet:business:user", uuid))
        self.redis.incr("monet:business:current:" + userId)
        if (int(self.redis.get("monet:business:current:" + userId)) > int(
                self.redis.hget("monet:business:max", userId))):
            return False
        return True

    def process_item(self, item, spider):

        data = dict(item)

        try:
            self.lock.acquire()
            CLOSESPIDER_ITEMCOUNT = int(spider.settings['taskdict'].get('CLOSESPIDER_ITEMCOUNT'))
            if CLOSESPIDER_ITEMCOUNT is -1 or int(spider.crawler.stats.get_value("collectNum")) < CLOSESPIDER_ITEMCOUNT:
                if str(spider.uuid).startswith("TEST"):
                    self.redis.sadd(self.name + spider.uuid, json.dumps(data, ensure_ascii=False))
                    spider.crawler.stats.inc_value("collectNum")
                elif self.business(spider.uuid):
                    keys = ', '.join(data.keys())
                    values = ', '.join(['%s'] * len(data))

                    tableName = str(spider.settings['taskdict'].get('tableName'))
                    sql = 'insert into %s (%s) values (%s)' % (tableName, keys, values)
                    try:
                        self.db.ping(reconnect=True)
                        self.db.cursor().execute(sql, tuple(data.values()))
                        self.db.commit()
                        spider.crawler.stats.inc_value("collectNum")
                    except Exception as e:
                        print(e)
                    finally:
                        self.db.rollback()
        finally:
            self.lock.release()
        return item
