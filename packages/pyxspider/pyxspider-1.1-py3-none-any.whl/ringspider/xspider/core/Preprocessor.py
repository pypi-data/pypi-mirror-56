# -*- coding: utf-8 -*-

import datetime
from ringspider.xspider.utils.exceptions import ParamError
from ringspider.xspider.core.Xspider import IncrementParam, Xspider
from ringspider.xspider.utils.defaults import SpiderTypeValue, XSpiderType


class UrlPreprocessor:
    """
    定义预处理器结构
    """

    def __init__(self, xspider, taskdict):
        self.entryUrls = xspider.entryUrls
        self.params = xspider.params
        self.incrementParam = xspider.config.incrementParam
        self.taskdict = taskdict

    def __system_process(self):
        """
        解析系统参数 date page keyword
        :return:url
        """
        for param in self.params:
            if param.name.__eq__('date'):
                self.__generate_date_url(param.begin, param.end, param.format)
            elif param.name.__eq__('page'):
                self.__generate_page_url(int(param.begin), int(param.end), int(param.step))
            elif param.name.__eq__('keyword'):
                self.__generate_keyword_url(param.value.split(' '))
        for i in range(len(self.params) - 1, -1, -1):
            if self.params[i].name.__eq__('date') or self.params[i].name.__eq__('page') or self.params[i].name.__eq__(
                    'keyword'):
                self.params.pop(i)

    def __generate_date(self, begin, end, format):
        st = datetime.datetime.strptime(begin, "%Y-%m-%d")
        et = datetime.datetime.strptime(end, "%Y-%m-%d")
        for i in range((et - st).days + 1):
            day = (st + datetime.timedelta(days=i)).strftime(format)
            yield day

    def __generate_date_url(self, begin, end, format):
        urls = []
        for url in self.entryUrls:
            if not url.__contains__('{date}'):
                urls.append(url)
                continue
            for i in self.__generate_date(begin, end, format):
                urls.append(url.replace('{date}', i))
        self.entryUrls = urls

    def __generate_page_url(self, begin, end, step):
        urls = []
        for url in self.entryUrls:
            if not url.__contains__('{page}'):
                urls.append(url)
                continue
            for i in range(begin, end + 1, step):
                urls.append(url.replace('{page}', str(i)))
        self.entryUrls = urls

    def __generate_keyword_url(self, keywords):
        urls = []
        for url in self.entryUrls:
            if not url.__contains__('{keyword}'):
                urls.append(url)
                continue
            for keyword in keywords:
                urls.append(url.replace('{keyword}', keyword))
        self.entryUrls = urls

    def __general_process(self):
        """
        处理器扩展
        :return:
        """
        for param in self.params:
            for index, url in enumerate(self.entryUrls):
                if url.__contains__('{' + param.name + '}'):
                    self.entryUrls[index] = url.replace('{' + param.name + '}', str(param.value))

    def __eq_ic(self, s1=None, s2=None):
        if s1 is None and ''.join(str(s1).split()) and s2 is None and ''.join(str(s2).split()):
            return False
        return s1.upper().__eq__(s2.upper())

    def __increment_process(self):
        if self.incrementParam is None:
            # 解析xspider类型  然后设置默认值
            self.__xspidertype()

        for param in self.params:
            if self.__eq_ic(self.incrementParam.key, XSpiderType.DATE.name) and \
                    self.__eq_ic(param.name, XSpiderType.DATE.name):
                param.end = datetime.datetime.now().strftime("%Y-%m-%d")
                d = -1
                try:
                    d = -1 * int(self.incrementParam.value)
                except Exception as e:
                    print(e)
                param.begin = (datetime.datetime.now() + datetime.timedelta(days=d)).strftime("%Y-%m-%d")
            elif self.__eq_ic(self.incrementParam.key, XSpiderType.PAGE.name) and \
                    self.__eq_ic(param.name, XSpiderType.PAGE.name):
                param.begin = 1
                p = 1
                try:
                    p = int(self.incrementParam.value)
                except Exception as e:
                    print(e)
                param.end = p
            elif self.__eq_ic(self.incrementParam.key, XSpiderType.GENERAL.name):
                if self.taskdict['CLOSESPIDER_ITEMCOUNT'] is None:
                    self.taskdict['CLOSESPIDER_ITEMCOUNT']=int(self.incrementParam.value)
                pass

    def __missing_process(self):
        self.entryUrls = None

    def __spidertype_process(self):
        """
        增量时处理传递过来的参数，根据xspider的config.incrementParam
        PAGE：获取前几页
        DATE：获取近几日
        GENERAL：获取近几条
        :return:
        """
        if self.__eq_ic(self.taskdict['spiderTypeValue'], SpiderTypeValue.INCREMENTAL.name):
            # 增量采集
            self.__increment_process()
        elif self.__eq_ic(self.taskdict['spiderTypeValue'], SpiderTypeValue.MISSING.name):
            # 缺失采集 去除所有参数 不由xml自动生成url 由用户加入starturls
            self.__missing_process()

    def __param_contains(self, name):
        for param in self.params:
            if self.__eq_ic(param.name, name):
                return True
        return False

    def __xspidertype(self):
        '''
        获取xspider的类型 PAGE DATE
        :return:
        '''
        if self.incrementParam is None:
            # 解析xspider类型  然后设置默认值
            if self.__param_contains(XSpiderType.DATE.name):
                self.incrementParam = IncrementParam(XSpiderType.DATE.name, 1)
            elif self.__param_contains(XSpiderType.PAGE.name):
                self.incrementParam = IncrementParam(XSpiderType.PAGE.name, 1)
            else:
                self.incrementParam = IncrementParam(XSpiderType.GENERAL.name, 100)
        else:
            # TODO 一致性检查,incrementParam和parms的内容匹配
            pass

    @classmethod
    def get_urls(cls, xspider, taskdict):
        """
        定义处理过程
        :return:
        """
        if not isinstance(xspider, Xspider):
            raise ParamError(message='xspider not a Xspider object')
        if not isinstance(taskdict, dict):
            raise ParamError(message='taskdict not a dict')
        o = cls(xspider, taskdict)
        o.__spidertype_process()
        o.__system_process()
        o.__general_process()
        for url in o.entryUrls:
            yield url


class GeneralUrlPreprocessor(UrlPreprocessor):

    @classmethod
    def process(cls, xspider, taskdict):
        pass
