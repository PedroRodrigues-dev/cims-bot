import asyncio
import discord
from configs.environment import discordToken
from tools import servers, channels, alerts, commands

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)


async def alert():
    while 1:
        alert = alerts.recive()

        if alert:
            alertChannelId = channels.getAlert()
            alertChannel = client.get_channel(int(alertChannelId.decode()))
            await alertChannel.send(alert["body"])

        await asyncio.sleep(2)


@client.event
async def on_ready():
    print(f"We have logged in as {client.user}")
    alerts.send("CIMS-BOT Started")
    client.loop.create_task(alert())


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content == "#servers-status":
        await message.channel.send(commands.serversStatus())
        return

    if message.content == "#set-alert-channel":
        await message.channel.send(commands.setAlertChannel(message))
        return

    if message.content.startswith("#"):
        await message.channel.send(commands.serverCommands(message))
        return


def run():
    client.run(discordToken())
