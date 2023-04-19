from configs import redis


def get(serverName):
    return redis.getValue(f"server::status::{serverName}")


def set(serverName, status):
    redis.setValue(f"server::status::{serverName}", status)
