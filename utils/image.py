import os
from io import BytesIO

from discord.ext import commands

import aiofile
import discord
import numpy as np
from PIL import Image, UnidentifiedImageError
from asyncdagpi import ImageFeatures

from utils.context import ApolloContext
from utils.metrics import isImage


async def dagpi_process(ctx: ApolloContext, image, feature, **kwargs) -> discord.Embed:
    """A method that uses dagpi to process images."""
    img = await ctx.bot.dagpi.image_process(getattr(ImageFeatures, feature)(), url=str(image), **kwargs)
    file = discord.File(img.image, f"{ctx.command.name}.{img.format}")
    await ctx.reply(file=file, can_delete=True)


async def urlToBytes(ctx, url) -> BytesIO:
    """A method that fetches bytes from a url."""
    response = await ctx.bot.session.get(url)
    byte = await response.read()
    if byte.__sizeof__() > 10 * (2**20):
        raise commands.BadArgument("Exceeded 10MB.")
    blob = BytesIO(byte)
    blob.seek(0)
    return blob


def fileFromBytes(ctx, image) -> discord.File:
    """A method that creates a file from bytes."""
    buffer = BytesIO()
    image.save(buffer, "png")
    buffer.seek(0)
    return discord.File(buffer, f"{ctx.command.name}.png")


async def process_minecraft(bot, b: BytesIO, quality=64) -> BytesIO:
    """A method that creates an image from minecraft blocks."""
    minecraft_array = np.array(list(bot.minecraft_blocks.keys()))
    np.expand_dims(minecraft_array, axis=-1)
    image = Image.open(b)
    image = image.convert("RGBA").resize((quality, quality))
    with Image.new("RGBA", (image.width * 16, image.height * 16)) as final_image:
        arr = np.asarray(image)
        np.expand_dims(arr, axis=-1)
        for y, r in enumerate(arr):
            for x, c in enumerate(r):
                difference = np.sqrt(
                    np.sum((minecraft_array - c) ** 2, axis=1))
                where = np.where(difference == np.amin(difference))
                to_paste = bot.minecraft_blocks[tuple(
                    minecraft_array[where][0])]
                final_image.paste(to_paste, (x * 16, y * 16), to_paste)
    buffer = BytesIO()
    final_image.save(buffer, "PNG")
    buffer.seek(0)
    return buffer


async def create_minecraft_blocks(bot) -> None:
    """A method that iterates through all the minecraft textures."""
    for _file in os.listdir("assets/minecraft_blocks"):
        async with aiofile.async_open("assets/minecraft_blocks/" + _file, "rb") as afp:
            b = await afp.read()
            await resize_and_save_minecraft_blocks(bot, BytesIO(b))


async def resize_and_save_minecraft_blocks(bot, b) -> None:
    """A method that resizes an image for minecraft command."""
    try:
        with Image.open(b) as image:
            image = image.convert("RGBA")
            bot.minecraft_blocks[image.resize(
                (1, 1)).getdata()[0]] = image
    except UnidentifiedImageError:
        pass
