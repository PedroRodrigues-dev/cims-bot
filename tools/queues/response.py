from configs import broker


def send(authorId, channelId, body):
    message = {
        "authorId": authorId,
        "channelId": channelId,
        "body": body,
    }

    return broker.sendMessage("responses", message)
