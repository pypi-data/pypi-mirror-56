# -*- coding: utf-8 -*-
import json
import random
import string
from xspider.utils.task import start_task, stop_task, finish_task, obj_dic
from xspider.utils.xmlparse import read_file_as_str


class MTSpiderClient:

    def start(self, uuid, task_dict, file_path):
        xml = read_file_as_str(file_path)
        start_task(uuid, xml, task_dict)

    def stop(self, uuid):
        stop_task(uuid)

    def finish(self, uuid):
        finish_task(uuid)


def main():
    file_path = "../xml/有数据的增量xml/成都商报.xml"
    maxcount = str(random.randint(12, 15))
    print(maxcount)
    task_dict = {
        "CLOSESPIDER_TIMEOUT": None,
        "CLOSESPIDER_ITEMCOUNT": maxcount,
        "CLOSESPIDER_PAGECOUNT": None,
        "CLOSESPIDER_ERRORCOUNT": None,
        "ldate": "2019-08-02",
        "edate": "2019-08-02",
        "startpage": 1,
        "endpage": 2,
        "spiderTypeValue": 'INCREMENTAL',
        "xSpiderTypeValue": "",
    }
    # INCREMENTAL  COMMON

    task_json = json.dumps(task_dict)
    uuid = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(8))
    client = MTSpiderClient()
    client.start(uuid, task_json, file_path)
    # stop()
    # finish()

    pass


if __name__ == '__main__':
    main()
