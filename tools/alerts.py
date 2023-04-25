from configs import broker
from tools import channels


def send(message):
    if channels.getAlert():
        return broker.sendMessage("alerts", {"body": message})
