from tools import servers, channels
from tools.queues import bot, server


def serversStatus():
    serversList = servers.getList()

    if serversList:
        return serversList
    else:
        return "no server registered"


def setAlertChannel(message):
    channels.setAlert(message.channel.id)

    return "now this channel will receive the alerts"


def serverCommands(message):
    messageArray = message.content.replace("#", "").split(" ")

    serverName = messageArray[0]

    if serverName not in servers.getOnlineList():
        return "the server is offline or cannot be found"

    messageArray.pop(0)
    messageBody = " ".join(messageArray)

    queueMessage = {
        "author_id": message.author.id,
        "command": messageBody,
    }

    if not bot.sendMessage(serverName, queueMessage):
        return "could not send message to server"

    queueResponse = server.reciveMessage(serverName)

    if not queueResponse:
        return "could not get response from server"

    return queueResponse["body"]
