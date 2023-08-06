from enum import Enum, unique
from scrapy.utils.project import get_project_settings
from xspider.utils.connection import RedisPool

spider_clear = object()
spider_stop = object()
spider_finish = object()
PROXY_NUM = 5
PROXY_ENABLE = True

NAME = 'monet'
PROXY_KEY = '%s:proxy' % NAME
XML_KEY = '%s:xml' % NAME
PARAM_KEY = '%s:param' % NAME

WAIT_KEY = '%s:wait' % NAME
RUN_KEY = '%s:run' % NAME
STOP_KEY = '%s:stop' % NAME
STOPED_KEY = '%s:stoped' % NAME
FINISH_KEY = '%s:finish' % NAME
FINISHED_KEY = '%s:finished' % NAME
ERROR_KEY = '%s:error' % NAME
key_list = [PROXY_KEY, XML_KEY, PARAM_KEY, WAIT_KEY, RUN_KEY, STOP_KEY, STOPED_KEY, FINISH_KEY, FINISHED_KEY, ERROR_KEY]

settings = get_project_settings()


manage = settings.get("MANAGE")
print(manage)
REDIS_HOST = manage.get("REDIS_HOST", "localhost")
REDIS_PORT = manage.get("REDIS_PORT", "6379")

redispool = RedisPool(REDIS_HOST, REDIS_PORT)
redis = redispool.redis()
PROXY_API = 'http://webapi.http.zhimacangku.com/getip?num=1&type=2&pro=320000&city=320100&yys=0&port=1&time=1&ts=1&ys=0&cs=0&lb=1&sb=0&pb=4&mr=1&regions='
PROXY_API_TIMEOUT = 5


@unique
class SpiderTypeValue(Enum):
    INCREMENTAL = 0
    MISSING = 1
    COMMON = 2


@unique
class XSpiderType(Enum):
    DATE = 0
    PAGE = 1
    GENERAL = 2
