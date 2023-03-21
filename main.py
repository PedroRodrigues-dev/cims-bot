from threading import Thread
import discord

from configs.environment import discordToken

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print(f"We have logged in as {client.user}")


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content == "#hello":
        await message.channel.send("Hello World!")


def main():
    Thread(target=client.run(discordToken()))


if __name__ == "__main__":
    main()
