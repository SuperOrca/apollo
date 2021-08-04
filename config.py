import discord


VIEW_TIMEOUT = 180

TOKEN = "ODQ3NTY2NTM5NjA3NzY5MDg5.YK_72g.g4YzW2p8vDdMQ-bNxdeTctZNuTk"
DAGPI = "MTYyMjkxOTE5Mw.DX0xYiXv3Et6R1LgoaTNS6iXQJ8PPecM.0b8cc770636b2e1a"
PREFIX = 'a!'
OWNER_IDS = (331179093447933963,)
COLOR = 0x2e4256

DESCRIPTION = """
An open-source general-use discord.py bot.
"""

NEWS_TITLE = ":newspaper: August 4, 2021"
NEWS_VALUE = """
jotte sus
"""

INTENTS = discord.Intents(
    guilds=True,
    members=True,
    bans=True,
    emojis=True,
    voice_states=True,
    messages=True,
    reactions=True
)

MENTIONS = discord.AllowedMentions.none()

STRIP_AFTER_PREFIX = True
CASE_INSENSITIVE = True
MAX_MESSAGES = 10000