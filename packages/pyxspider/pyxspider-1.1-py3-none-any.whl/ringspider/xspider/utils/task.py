from ringspider.xspider.utils.defaults import redis, WAIT_KEY, XML_KEY, PARAM_KEY, STOP_KEY, FINISH_KEY


def set_wait(uuid):
    redis.sadd(WAIT_KEY, uuid)


def set_xml(uuid, xml):
    redis.hset(XML_KEY, uuid, xml)


def set_param(uuid, param):
    redis.hset(PARAM_KEY, uuid, param)


def start_task(uuid, xml, param):
    set_wait(uuid)
    set_xml(uuid, xml)
    set_param(uuid, param)


def stop_task(uuid):
    redis.sadd(STOP_KEY, uuid)


def finish_task(uuid):
    redis.sadd(FINISH_KEY, uuid)


def obj_dic(d):
    top = type('new', (object,), d)
    seqs = tuple, list, set, frozenset
    for i, j in d.items():
        if isinstance(j, dict):
            setattr(top, i, obj_dic(j))
        elif isinstance(j, seqs):
            setattr(top, i,
                    type(j)(obj_dic(sj) if isinstance(sj, dict) else sj for sj in j))
        else:
            setattr(top, i, j)
    return top
