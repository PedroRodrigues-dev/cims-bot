from configs import redis


def get(serverName):
    value = redis.getValue(f"server::status::{serverName}")

    if value:
        value = value.decode()

    return value


def set(serverName, status):
    if get(serverName) != status:
        redis.setValue(f"server::status::{serverName}", status)
