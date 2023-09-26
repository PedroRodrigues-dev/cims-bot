import os
from tools import servers, channels
from tools.queues import bot, response


async def interpreter(client, message):
    if message.author == client.user:
        return

    if message.content == "#servers-status":
        serversStatus(message)
        return

    if message.content == "#set-alert-channel":
        setAlertChannel(message)
        return

    if message.content.startswith("#define-routine"):
        await defineRoutine(message)
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


async def defineRoutine(message):
    authorId = message.author.id
    channelId = message.channel.id

    if not message.attachments:
        response.send(
            authorId,
            channelId,
            "you need to send a file to define a routine",
        )
        return

    for attachment in message.attachments:
        if not attachment.filename.endswith(".tila"):
            response.send(
                authorId,
                channelId,
                f"{attachment.filename} - Invalid file type, only TimeLang scripts are accepted",
            )
            return

        fileContent = await attachment.read()

        messageArray = message.content.split(" ")
        serverName = messageArray[1]

        messageBody = {
            "code": fileContent.decode(),
        }

        body = f"{attachment.filename} - Accepted"

        if not bot.sendMessage(serverName, authorId, channelId, messageBody):
            body = "could not send message to server"

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
