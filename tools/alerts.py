from configs import broker


def send(message):
    return broker.sendMessage("alerts", {"body": message})


def recive():
    return broker.reciveMessage("alerts")
