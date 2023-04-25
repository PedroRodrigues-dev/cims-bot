import asyncio
import json
import discord
from configs import broker, environment
from tools import channels, alerts, commands

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

_connection = broker.getConnection()


async def response():
    channel = _connection.channel()

    while True:
        channel.queue_declare(queue="responses", durable=True)

        methodFrame, headerFrame, body = channel.basic_get(
            queue="responses", auto_ack=True
        )

        if methodFrame:
            body = json.loads(body.decode())

            alertChannel = client.get_channel(int(body["channelId"]))
            await alertChannel.send(body["body"])

        await asyncio.sleep(1)


@client.event
async def on_ready():
    print(f"We have logged in as {client.user}")
    alerts.send("CIMS-BOT Started")
    client.loop.create_task(response())


@client.event
async def on_message(message):
    commands.interpreter(client, message)


def run():
    client.run(environment.discordToken())
