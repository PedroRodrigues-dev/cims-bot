from configs import redis


def getOnlineList():
    keys = redis.getKeys("server::status::*")
    values = redis.getMultiValues(keys)

    results = []
    for k, v in zip(keys, values):
        if v == b"online":
            key_str = k.decode().replace("server::status::", "")
            results.append(f"{key_str}: {v.decode()}")

    return "\n".join(results)


def getList():
    keys = redis.getKeys("server::status::*")
    values = redis.getMultiValues(keys)

    result = "\n".join(
        [
            f'{key.decode().replace("server::status::", "")} ({value.decode()})'
            for key, value in zip(keys, values)
        ]
    )

    return result


def getNames():
    keys = redis.getKeys("server::status::*")
    result = [key.decode().replace("server::status::", "") for key in keys]
    return result
