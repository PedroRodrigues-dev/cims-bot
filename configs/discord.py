import asyncio
import discord
from configs.environment import discordToken
from tools import servers, channels, alerts
from tools.queues import bot, server

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)


async def alert():
    while 1:
        alertChannelId = channels.getAlert()

        if alertChannelId:
            alertChannel = client.get_channel(int(alertChannelId.decode()))

            alert = alerts.recive()

            if alert:
                await alertChannel.send(alert["body"])

        await asyncio.sleep(2)


@client.event
async def on_ready():
    print(f"We have logged in as {client.user}")

    client.loop.create_task(alert())

    alertChannelId = channels.getAlert()

    if alertChannelId:
        alertChannel = client.get_channel(int(alertChannelId.decode()))

        await alertChannel.send("CIMS-BOT Started")


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content == "#servers-status":
        serversList = servers.getList()

        if serversList:
            await message.channel.send(serversList)
        else:
            await message.channel.send("no server registered")

        return

    if message.content == "#set-alert-channel":
        channels.setAlert(message.channel.id)

        await message.channel.send(f"now this channel will receive the alerts")

        return

    if message.content.startswith("#"):
        messageWithoutHashtag = message.content.replace("#", "")
        messageArray = messageWithoutHashtag.split(" ")

        serverName = messageArray[0]

        if serverName not in servers.getOnlineList():
            await message.channel.send("the server is offline or cannot be found")
            return

        messageArray.pop(0)
        messageBody = " ".join(messageArray)

        queueMessage = {
            "author_id": message.author.id,
            "command": messageBody,
        }

        if not bot.sendMessage(serverName, queueMessage):
            await message.channel.send("could not send message to server")
            return

        queueResponse = server.reciveMessage(serverName)

        if not queueResponse:
            await message.channel.send("could not get response from server")
            return

        await message.channel.send(queueResponse["body"])


def run():
    client.run(discordToken())
