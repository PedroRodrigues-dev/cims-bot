import redis


r = redis.Redis(host="localhost", port=6379, db=0)


def setValue(key, value):
    r.set(key, value)


def getValue(key):
    return r.get(key)


def getKeys(key):
    return r.keys(key)


def getMultiValues(keys):
    return r.mget(keys)
