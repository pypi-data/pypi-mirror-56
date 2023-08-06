# -*- coding: utf-8 -*-


import datetime
import re
from urllib.parse import urljoin
from scrapy import Request, Item, Field
from scrapy_redis.spiders import RedisSpider
from scrapy.exceptions import NotConfigured

from xspider.core.Xspider import Xspider

from xspider.core.Preprocessor import UrlPreprocessor

from xspider.utils.defaults import *
from xspider.utils.parser import AriticleParser


class XspiderSpider(RedisSpider):
    name = "xspider"
    # lpush xspider:start_urls https://baidu.com/s?rtt=1&bsst=1&cl=2&tn=news&rsv_dl=ns_pc&word=site:(www.people.com.cn)两会
    # redis_key = name + ':start_urls'
    allowed_domains = []
    # start_urls = ['https://image.so.com/z?ch=beauty']
    # 系统配置
    custom_settings = {

    }

    def __init__(self, uuid, *args, **kwargs):
        self.uuid = uuid

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        uuid = kwargs.get('uuid', None)
        if uuid is None:
            raise NotConfigured
        obj = super(XspiderSpider, cls).from_crawler(crawler, *args, **kwargs)
        try:
            obj._set_task()
        except Exception as e:
            print(e)
            raise NotConfigured
        else:
            return obj

    def start_requests(self):
        for url in UrlPreprocessor.get_urls(self.xspider, self.taskdict):
            yield Request(url, self.parse)

    def abshref(self, url, link):
        return urljoin(url, link)

    def okpageextractors(self, pageextractors, url):
        current_pageextractors = []
        for pageextractor in pageextractors:
            if re.match(pageextractor.urlRegex, url):
                current_pageextractors.append(pageextractor)
        return current_pageextractors

    def parse(self, response):
        '''
        解析页面数据
        :param response:
        :return:
        '''

        monet_item = Item()
        self.update_item(response, monet_item)

        pageextractors = self.xspider.pageextractors
        current_pageextractors = self.okpageextractors(pageextractors, response.url)
        for index, pageextractor in enumerate(current_pageextractors):

            datastored = pageextractor.dataStored
            last = index == len(current_pageextractors) - 1
            hasregion = bool(pageextractor.region)
            self.parse_col(response, response, pageextractor, monet_item)
            for link in self.parse_link(response, response, pageextractor, monet_item, datastored, False):
                yield link

            for oregion in pageextractor.region:
                for region in response.xpath(oregion.xpath):
                    r_monet_item = Item()
                    r_monet_item.update(monet_item)
                    self.parse_col(response, region, oregion, r_monet_item)

                    for link in self.parse_link(response, region, oregion, r_monet_item, datastored, True):
                        yield link
                    if datastored and (last or not self.hasNoneCol(r_monet_item)):
                        yield r_monet_item
            nonecol = self.hasNoneCol(monet_item)
            if not hasregion and datastored and (last or not nonecol):
                yield monet_item

    def update_item(self, response, monet_item):
        if response.meta.__contains__("item"):
            for key in response.meta["item"].keys():
                monet_item.fields[key] = Field()
            monet_item.update(response.meta["item"])

        monet_item.fields['url'] = Field()
        monet_item['url'] = response.url

    def parse_link(self, response, selector, extract, monet_item, datastored=False, isinner=False):
        '''
        解析链接
        :param response:
        :param selector:
        :param extract:
        :param monet_item:
        :param datastored:
        :param isinner:
        :return:
        '''
        url = response.url
        for olink in extract.links:
            links = selector.xpath(olink.xpath).getall()
            if not datastored and isinner:
                for link in links:
                    yield Request(self.abshref(url, link), callback=self.parse, meta={"item": monet_item})
            else:
                for link in links:
                    yield Request(self.abshref(url, link), callback=self.parse)

    def parse_col(self, response, selector, extract, monet_item):
        '''
        解析字段
        :param response:
        :param selector:
        :param extract:
        :param monet_item:
        :return:
        '''
        for osetcol in extract.setcols:
            setcol = None
            if Xspider.special_xpath(osetcol.xpath):
                # TODO
                setcol = self.special_parser(osetcol.xpath, selector, monet_item)
                pass
            else:
                try:
                    setcol = '\n'.join(selector.xpath(osetcol.xpath).getall())
                except Exception as e:
                    print(e)

            if setcol is not None:
                setcol = self.clear(setcol, osetcol)

            monet_item.fields[osetcol.ref] = Field()
            monet_item[osetcol.ref] = setcol

    def special_parser(self, xpath, selector, monet_item):
        ariticleParser = AriticleParser()
        if xpath.__eq__('CONTENT'):
            tt = ariticleParser.extract_title(selector.text)
            return ariticleParser.extract_content(selector.text, tt)
        if xpath.__eq__('SOURCE'):
            return ariticleParser.extract_source(selector.text)
        if xpath.__eq__('URL'):
            return monet_item['url']
        if xpath.__eq__('TITLE'):
            return ariticleParser.extract_title(selector.text)
        if xpath.__eq__('PUBTIME'):
            return ariticleParser.extract_pubtime(selector.text)

        return None

    def clear(self, str, selector):
        '''
        格式化
        :param str:
        :param selector:
        :return:
        '''
        regex = selector.regex
        if regex is None:
            return str
        str = re.sub("\\n", "", str)
        gs = re.search(regex, str)
        format = selector.format
        if gs:
            if format and re.match("{\d+}", format):
                format = format.replace("{0}", gs.group())
                for i, group in enumerate(gs.groups()):
                    format = format.replace("{" + (i + 1).__str__() + "}", group)
                return format
            else:
                return gs.group()
        return str

    def _set_task(self):
        try:
            xmlstr = redis.hget(XML_KEY, self.uuid)
            self.xspider = Xspider(xmlstr)
            self.taskdict = self.settings['taskdict']
            self.name = NAME + ":" + self.uuid
            self.redis_key = self.name + ':start_urls'
        except Exception as e:
            print(e)

    def hasNoneCol(self, newsitem):
        for col in self.xspider.getNotNullColName():
            if newsitem.get(col, None) is None:
                return True
        return False
