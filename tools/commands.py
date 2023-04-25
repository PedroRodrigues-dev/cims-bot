from tools import servers, channels
from tools.queues import bot, response


def interpreter(client, message):
    if message.author == client.user:
        return

    if message.content == "#servers-status":
        serversStatus(message)
        return

    if message.content == "#set-alert-channel":
        setAlertChannel(message)
        return

    if message.content.startswith("#"):
        serverCommands(message)
        return


def serversStatus(message):
    authorId = message.author.id
    channelId = message.channel.id
    body = "no server registered"

    serversList = servers.getList()

    if serversList:
        body = serversList

    response.send(authorId, channelId, body)


def setAlertChannel(message):
    authorId = message.author.id
    channelId = message.channel.id
    body = "now this channel will receive the alerts"

    channels.setAlert(message.channel.id)

    response.send(authorId, channelId, body)


def serverCommands(message):
    authorId = message.author.id
    channelId = message.channel.id

    messageArray = message.content.replace("#", "").split(" ")
    serverName = messageArray[0]

    if serverName not in servers.getOnlineList():
        body = "the server is offline or cannot be found"

        response.send(authorId, channelId, body)

    messageArray.pop(0)
    messageBody = " ".join(messageArray)

    if not bot.sendMessage(serverName, authorId, channelId, messageBody):
        body = "could not send message to server"

        response.send(authorId, channelId, body)
