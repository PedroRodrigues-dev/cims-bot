import discord
from configs import rabbit
from configs.environment import discordToken
from tools import servers, channels
import json

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print(f"We have logged in as {client.user}")

    alertChannelId = channels.getAlert()

    if alertChannelId:
        alertChannel = client.get_channel(int(alertChannelId.decode()))

        await alertChannel.send("CIMS-BOT Started")


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content == "#servers-status":
        await message.channel.send(servers.getList())

        return

    if message.content == "#set-alert-channel":
        channels.setAlert(message.channel.id)

        await message.channel.send(f"now this channel will receive the alerts")

        return

    if message.content.startswith("#"):
        messageWithoutHashtag = message.content.replace("#", "")
        messageArray = messageWithoutHashtag.split(" ")

        serverName = messageArray[0]

        if serverName in servers.getOnlineList():
            messageArray.pop(0)

            messageBody = " ".join(messageArray)

            queueMessage = {
                "author_id": message.author.id,
                "command": messageBody,
            }

            rabbit.sendMessage(serverName, queueMessage)

            queueResponse = rabbit.reciveMessages(serverName)

            if isinstance(queueResponse, str):
                queueResponse = json.loads(queueResponse)

            await message.channel.send(queueResponse["body"])
        else:
            await message.channel.send("the server is offline or cannot be found")


def run():
    client.run(discordToken())
