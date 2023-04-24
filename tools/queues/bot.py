from configs import broker


def sendMessage(serverName, message):
    return broker.sendMessage(f"{serverName}-bot", message)
