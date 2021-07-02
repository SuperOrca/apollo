from typing import Union
import discord

from .http import geturljson


def isImage(url):
    url = url.lower()
    return bool(
        url.endswith("png")
        or url.endswith("jpg")
        or url.endswith("jpeg")
        or url.endswith("webp")
    )


async def get_pronoun(bot: Union[discord.Client, discord.ext.commands.Bot], member: discord.Member):
    pronouns = {
        "hh": "he/him",
        "hi": "he/it",
        "hs": "/he/she",
        "ht": "he/they",
        "ih": "it/him",
        "ii": "it/its",
        "is": "it/she",
        "it": "it/they",
        "shh": "she/he",
        "sh": "she/her",
        "si": "she/it",
        "st": "she/they",
        "th": "they/he",
        "ti": "they/it",
        "ts": "they/she",
        "tt": "they/them",
        "any": "Any",
        "other": "Other",
        "ask": "Ask",
        "avoid": "No pronoun, use name",
        "None": "N/A"
    }
    try:
        res = await geturljson(f"https://pronoundb.org/api/v1/lookup?id={member.id}&platform=discord")
    except Exception:
        return "Unavailable"
    try:
        code = res["pronouns"]
    except KeyError:
        code = "None"
    return pronouns[code]
