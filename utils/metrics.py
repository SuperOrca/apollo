from typing import Union
import discord

def isImage(url):
    url = url.lower()
    return bool(
        url.endswith("png")
        or url.endswith("jpg")
        or url.endswith("jpeg")
        or url.endswith("webp")
    )
