import os


def discordToken():
    return (
        os.getenv("CIMS_BOT_DISCORD_TOKEN")
        or "MTA4NzUyOTkzNzEzMDUwNDI3Mg.G7OYZP.rQKkgA6OaJcue9G516_QOeXw4UL6azOUfxgtyk"
    )
