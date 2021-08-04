import os
from io import BytesIO

import aiofile
import discord
import numpy as np
from PIL import Image, UnidentifiedImageError
from asyncdagpi import ImageFeatures
from discord.ext import commands

from utils.context import ApolloContext


async def dagpi_process(ctx: ApolloContext, image, feature, **kwargs) -> discord.Embed:
    """A method that uses dagpi to process images."""
    img = await ctx.bot.dagpi.image_process(getattr(ImageFeatures, feature)(), url=str(image), **kwargs)
    file = discord.File(img.image, f"{ctx.command.name}.{img.format}")
    await ctx.reply(file=file, can_delete=True)


async def urlToBytes(ctx, url) -> BytesIO:
    """A method that fetches bytes from a url."""
    response = await ctx.bot.session.get(url)
    byte = await response.read()
    if byte.__sizeof__() > 10 * (2 ** 20):
        raise commands.UserInputError("Exceeded 10MB.")
    blob = BytesIO(byte)
    blob.seek(0)
    return blob


def fileFromBytes(ctx, image) -> discord.File:
    """A method that creates a file from bytes."""
    buffer = BytesIO()
    image.save(buffer, "png")
    buffer.seek(0)
    return discord.File(buffer, f"{ctx.command.name}.png")
    