from configs import broker


def reciveMessage(serverName):
    return broker.reciveMessage(f"{serverName}-server")
