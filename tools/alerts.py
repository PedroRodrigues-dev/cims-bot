from tools import channels
from tools.queues import response


def send(message):
    alertsChannelId = channels.getAlert()

    if alertsChannelId:
        return response.send("cims-bot", alertsChannelId.decode(), message)
