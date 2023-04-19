import threading
from tools import keepAlive
from configs import discord


def main():
    threading.Thread(target=keepAlive.init).start()
    discord.run()


if __name__ == "__main__":
    main()
