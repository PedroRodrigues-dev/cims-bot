from configs import broker


def sendMessage(serverName, authorId, channelId, body):
    message = {
        "authorId": authorId,
        "channelId": channelId,
        "body": body,
    }

    return broker.sendMessage(serverName, message)
