# -*- coding: utf-8 -*-

from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, Join, Compose, MapCompose


class NewsLoader(ItemLoader):
    default_output_processor = MapCompose()
