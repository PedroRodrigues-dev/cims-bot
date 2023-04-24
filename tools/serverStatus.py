from configs import redis


def get(serverName):
    return redis.getValue(f"server::status::{serverName}").decode()


def set(serverName, status):
    if get(serverName) != status:
        redis.setValue(f"server::status::{serverName}", status)
