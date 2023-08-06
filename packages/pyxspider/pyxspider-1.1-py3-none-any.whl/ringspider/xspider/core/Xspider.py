# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET
from ringspider.xspider.utils.xmlparse import *


class Head:

    def __init__(self, xsid, name, description):
        self.xsid = xsid
        self.name = name
        self.description = description


class Param:

    def __init__(self, name="", label="", type="string", format=None, size=None, value=None, defaultValue=None,
                 notNull=True, begin=1, end=1, step=1):
        self.name = name
        self.label = label
        self.type = type
        if format is not None:
            self.format = format.replace('yyyy', '%Y').replace('MM', '%m').replace('dd', '%d')
        self.value = value
        self.defaultValue = defaultValue
        self.notNull = notNull
        self.begin = begin
        self.end = end
        self.step = step


class DataCol:
    def __init__(self, name=None, label=None, type="text", defaultValue=None, size=None, format=None, notNull=True):
        self.name = name
        self.label = label
        self.type = type
        self.defaultValue = defaultValue
        self.size = size
        self.format = format
        self.notNull = notNull

    pass


class Pageextractor:
    def __init__(self, name, dataStored=True, jsonRegex=None, sampleUrl=None, type="html", urlRegex=None, links=[],
                 setcols=[], regions=[]):
        self.name = name
        self.dataStored = dataStored
        self.jsonRegex = jsonRegex
        self.sampleUrl = sampleUrl
        self.type = type
        self.urlRegex = urlRegex
        self.links = links
        self.setcols = setcols
        self.region = regions


class Region:
    def __init__(self, name, label, xpath='.', regex=None, setcols=None, links=None):
        self.name = name
        self.label = label
        self.xpath = xpath
        self.regex = regex
        self.setcols = setcols
        self.links = links


class Node:
    def __init__(self, xpath='.', regex='(.*)', format='{1}'):
        self.xpath = xpath
        self.regex = regex
        self.format = format


class SetCol(Node):
    def __init__(self, ref=None, xpath='.', regex=None, format=None):
        super(SetCol, self).__init__(xpath, regex, format)
        self.ref = ref


class Link(Node):
    def __init__(self, name=None, label=None, xpath='.', regex='(.*)', format={1}):
        super(Link, self).__init__(xpath, regex, format)
        self.name = name
        self.label = label


class Config:
    def __init__(self, agent=0, cookie=None, urlcharset="utf-8", charset="utf-8", sleepInterval="1000",
                 antiVerfiedCodeType="auto", poolSize=2, threadNum=5, timeOut=10000, retryTimes=2, cycleRetryTimes=2,
                 incrementParam=None):
        self.agent = agent
        self.cookie = cookie
        self.urlcharset = urlcharset
        self.charset = charset
        self.sleepInterval = sleepInterval
        self.antiVerfiedCodeType = antiVerfiedCodeType
        self.poolSize = poolSize
        self.threadNum = threadNum
        self.retryTimes = retryTimes
        self.cycleRetryTimes = cycleRetryTimes
        self.incrementParam = incrementParam


class IncrementParam:
    def __init__(self, key=None, value=None):
        self.key = key
        self.value = value


class Xspider():

    # 从xspider解析得到scrapy spider所需的参数
    def __init__(self, str):
        self.str = str
        tree = readfromstr(self.str)
        self.root = tree.getroot()
        self.__head()
        self.__params()
        self.__entryUrls()
        self.__datastructures()
        self.__pageextractors()
        self.__config()
        self.dict = xmlstrtodict(self.str)
        self.datastructure = self.dict["xspider"]["body"]["datastructure"]

    '''
    head 
    '''

    def __findhead(self):
        return find_node(self.root, "head")

    def __head(self):
        self.head = Head(self.__xsid(), self.__name(), self.__description())

    def __xsid(self):
        return find_node(self.__findhead(), "xsid")

    def __name(self):
        return find_node(self.__findhead(), "name")

    def __description(self):
        return find_node(self.__findhead(), "description")

    '''
    body
    '''

    def __findbody(self):
        return find_node(self.root, "body")

    '''
    entry
    '''

    def __findentry(self):
        return find_node(self.root, "body/entry")

    def __entryUrls(self):
        self.entryUrls = []
        for entry in find_nodes(self.__findentry(), "entryUrls/entryUrl"):
            if entry.text is None:
                continue
            url = entry.text.strip()
            if url:
                self.entryUrls.append(url)

    def __params(self):
        self.params = []
        for node in find_nodes(self.__findentry(), "params/param"):
            self.params.append(Param(node.attrib.get("name", ""), label=node.attrib.get("label", None),
                                     type=node.attrib.get("type", None),
                                     format=node.attrib.get("format"), value=node.attrib.get("value", None),
                                     begin=node.attrib.get("begin"), end=node.attrib.get("end"),
                                     step=node.attrib.get("step")))

    '''
    datastructure
    '''

    def __not_empty(self, s1):
        if not s1 or not s1.strip():
            return True
        return True

    def __datastructures(self):
        self.datacols = []
        for node in find_nodes(self.__findbody(), "datastructure/col"):
            if self.__not_empty(node.attrib.get("name")):
                self.datacols.append(
                    DataCol(node.attrib.get("name"), label=node.attrib.get("label"), type=node.attrib.get("type"),
                            defaultValue=node.attrib.get("defaultValue"), size=node.attrib.get("size"),
                            format=node.attrib.get("format"), notNull=node.attrib.get("notNull")))

    def getNotNullColName(self):
        list = []
        for col in self.datastructure.get("col"):
            if str(col.get("@notNull", False)).__eq__("true"):
                list.append(col.get("@name"))
        return list

    '''
    pageextractors
    '''

    def __findpageextractors(self):
        return find_node(self.root, "body/pageextractors")

    def __pageextractors(self):
        self.pageextractors = []
        nodes = find_nodes(self.__findpageextractors(), "pageextractor")
        for node in nodes:
            regions = self.__regions(node)
            setcols = self.__setcols(node)
            links = self.__links(node)
            dataStored = False
            if node.attrib.get("dataStored").lower().__eq__('true'):
                dataStored = True
            self.pageextractors.append(
                Pageextractor(name=node.attrib.get("name"), dataStored=dataStored,
                              jsonRegex=node.attrib.get("jsonRegex"),
                              sampleUrl=node.attrib.get("sampleUrl"),
                              type=node.attrib.get("type"), urlRegex=node.attrib.get("urlRegex"),
                              links=links, setcols=setcols, regions=regions))

    '''
    
    '''

    def __regions(self, element):
        regions = []
        for node in find_nodes(element, "region"):
            setcols = self.__setcols(node, True)
            links = self.__links(node, True)
            xpath = self.__compatible_xpath(node.attrib.get("xpath"))
            regions.append(
                Region(node.attrib.get("name"), node.attrib.get("label"), xpath,
                       node.attrib.get("regex"), setcols=setcols, links=links))
        return regions

    def __setcols(self, element, inner=False):
        setcols = []
        for node in find_nodes(element, "setcol"):
            ref = node.attrib.get("ref")
            if ref is None:
                continue
            if inner:
                xpath = self.__inner_compatible_xpath(node.attrib.get("xpath"))
            else:
                xpath = self.__compatible_xpath(node.attrib.get("xpath"))
            setcols.append(
                SetCol(ref, xpath, node.attrib.get("regex"),
                       node.attrib.get("format")))
        return setcols

    def __links(self, element, inner=False):
        links = []
        for node in find_nodes(element, "link"):
            if inner:
                xpath = self.__inner_compatible_xpath(node.attrib.get("xpath"))
            else:
                xpath = self.__compatible_xpath(node.attrib.get("xpath"))
            # xpath = self.__compatible_xpath(node.attrib.get("xpath"))
            links.append(Link(node.attrib.get("name"), node.attrib.get("label"), xpath,
                              node.attrib.get("regex"), node.attrib.get("format")))
        return links

    '''
    config
    '''

    def __config(self):
        node = find_node(self.root, "body/config")
        incrementParam = None
        IPElement = node.find("incrementParam")
        if IPElement is not None and IPElement.attrib.get("key", None) is not None and IPElement.attrib.get("value",
                                                                                                            None) is not None:
            incrementParam = IncrementParam(IPElement.attrib.get("key", None),
                                            IPElement.attrib.get("value", None))


        self.config = Config( urlcharset=find_text(node,"urlcharset","utf-8"),
                             charset=find_text(node,"charset","utf-8"), sleepInterval=find_text(node,"sleep","1000"),
                             incrementParam=incrementParam)

    def __common_compatible_xpath(self, xpath):
        xpath = xpath.replace('@abs:href', '@href', 1)
        xpath = xpath.replace('contains(allText()', 'contains(string(.//text())')
        xpath = xpath.replace('//allText()', '//text()')
        xpath = xpath.replace('/allText()', '//text()')
        xpath = xpath.replace('allText()', '//text()')
        xpath = xpath.replace('//tidyText()', '//text()')
        xpath = xpath.replace('/tidyText()', '//text()')
        xpath = xpath.replace('tidyText()', '//text()')
        xpath = xpath.replace('/outerHtml()', '')
        xpath = xpath.replace('/html()', '')
        while xpath.endswith('/'):
            xpath = xpath[:-1]
        return xpath

    def __inner_compatible_xpath(self, xpath):
        if not xpath:
            return '.'
        if Xspider.special_xpath(xpath):
            return xpath
        if xpath.startswith('//'):
            xpath = xpath.replace('//', './/', 1)
        elif xpath.startswith('/'):
            xpath = xpath.replace('/', '', 1)
        else:
            xpath = '//' + xpath
        return self.__common_compatible_xpath(xpath)

    def __compatible_xpath(self, xpath):
        if not xpath:
            return '.'
        if Xspider.special_xpath(xpath):
            return xpath
        if xpath.startswith('//'):
            xpath = xpath.replace('//', './/', 1)
        return self.__common_compatible_xpath(xpath)

    @classmethod
    def special_xpath(self, xpath):
        if xpath.__eq__('CONTENT') or \
                xpath.__eq__('TITLE') or \
                xpath.__eq__('SOURCE') or \
                xpath.__eq__('URL') or \
                xpath.__eq__('TITLE') or \
                xpath.__eq__('PUBTIME'): \
                return True
        return False

    def elementstr(self):
        return str(ET.tostring(self.root, encoding='utf-8', method='xml'), "utf-8")
