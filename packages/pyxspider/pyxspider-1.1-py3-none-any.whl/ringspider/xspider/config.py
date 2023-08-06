# -*- coding: utf-8 -*-


import json
import logging
from ringspider.xspider.utils.defaults import SpiderTypeValue
from ringspider.xspider.utils.log import initLogger

logger = logging.getLogger(__name__)
initLogger()


class SpiderConfig:
    def __init__(self, xspider, taskConfig):
        self.xspider = xspider
        self.taskConfig = taskConfig


class TaskConfig:

    def __init__(self, task_json=None):

        task_dict = self._parse(task_json)
        if isinstance(task_dict, dict):
            self.dict = task_dict
        else:
            self.dict = {
                "CLOSESPIDER_TIMEOUT": None,
                "CLOSESPIDER_ITEMCOUNT": None,
                "CLOSESPIDER_PAGECOUNT": None,
                "CLOSESPIDER_ERRORCOUNT": None,
                "ldate": "2019-08-02",
                "edate": "2019-08-02",
                "startpage": "1",
                "endpage": "2",
                "spiderTypeValue": SpiderTypeValue.COMMON,
                "xSpiderTypeValue": "",
            }
        pass

    def _parse(self, task_json):
        try:
            task_dict = json.loads(task_json)
        except Exception as e:
            print(e)
            return None
        else:
            return task_dict
        return

    pass
