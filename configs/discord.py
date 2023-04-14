import discord
from configs import rabbit
from configs.environment import discordToken

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

servers = ["pop-os"]


@client.event
async def on_ready():
    print(f"We have logged in as {client.user}")


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith("#"):
        messageWithoutHashtag = message.content.replace("#", "")
        messageArray = messageWithoutHashtag.split(" ")

        serverName = messageArray[0]

        if serverName in servers:
            messageArray.pop(0)

            messageBody = " ".join(messageArray)

            queueMessage = {
                "author_id": message.author.id,
                "command": messageBody,
            }

            rabbit.sendMessage(serverName, queueMessage)


def run():
    client.run(discordToken())
