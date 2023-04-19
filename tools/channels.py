from configs import redis


def setAlert(channelId):
    redis.setValue("bot::channel::alert", channelId)


def getAlert():
    return redis.getValue("bot::channel::alert")
