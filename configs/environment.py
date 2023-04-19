import os


def discordToken():
    return os.getenv("CIMS_BOT_DISCORD_TOKEN")


def systemTimeout():
    return os.getenv("CIMS_BOT_SYSTEM_TIMEOUT") or 5


def rabbitUsername():
    return os.getenv("CIMS_BOT_RABBIT_USERNAME") or "guest"


def rabbitPassword():
    return os.getenv("CIMS_BOT_RABBIT_PASSWORD") or "guest"


def rabbitHost():
    return os.getenv("CIMS_BOT_DISCORD_RABBIT_HOST") or "localhost"
