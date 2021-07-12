import re
from typing import Union
from io import BytesIO

import discord
from discord.ext import commands
from PIL import Image, UnidentifiedImageError
import twemoji_parser as twemoji
import numpy as np
import os
import aiofile

from .metrics import isImage


async def dagpi_process(ctx: commands.Context, image, feature, end="png", **kwargs) -> discord.Embed:
    url = await getImage(ctx, image)
    async with ctx.typing():
        img = await ctx.bot.dagpi.image_process(feature, url=str(url), **kwargs)
        file = discord.File(img.image, f"{ctx.command.name}.{end}")
        embed = discord.Embed(color=discord.Color.dark_blue())
        embed.set_image(url=f"attachment://{ctx.command.name}.{end}")
        embed.set_footer(text="Powered by https://dagpi.xyz/")
    await ctx.reply(file=file, embed=embed)


async def imageToPIL(ctx, image) -> Image:
    url = await getImage(ctx, image)
    response = await ctx.bot.session.get(url)
    return Image.open(BytesIO(await response.read()))


def fileFromBytes(ctx, image) -> discord.File:
    buffer = BytesIO()
    image.save(buffer, "png")
    buffer.seek(0)
    return discord.File(buffer, f"{ctx.command.name}.png")


async def getImage(ctx: commands.Context, url: Union[discord.Member, discord.Emoji, discord.PartialEmoji, None, str] = None):

    if isinstance(url, str):
        url = await twemoji.emoji_to_url(url)

    if ctx.message.reference:
        ref = ctx.message.reference.resolved
        if ref.embeds:
            if ref.embeds[0].image.url != discord.Embed.Empty and isImage(
                ref.embeds[0].image.url
            ):
                return ref.embeds[0].image.url

            if ref.embeds[0].thumbnail.url != discord.Embed.Empty and isImage(
                ref.embeds[0].thumbnail.url
            ):
                return ref.embeds[0].thumbnail.url

        elif ref.attachments:
            url = ref.attachments[0].url or ref.attachments[0].proxy_url
            if isImage(url):
                return url

    if isinstance(url, discord.Member):
        return str(url.avatar.url)
    elif isinstance(url, str):
        if re.search(
            r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*(),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+",
            url,
        ) and isImage(url):
            return url

    if isinstance(url, (discord.Emoji, discord.PartialEmoji)):
        return url.url

    if ctx.message.attachments:

        url = ctx.message.attachments[0].url or ctx.message.attachments[0].proxy_url

        if isImage(url):
            return ctx.message.attachments[0].proxy_url or ctx.message.attachments[0].url

        elif isinstance(url, discord.Member):
            return str(url.avatar.url)
        else:
            return str(ctx.author.avatar.url)

    if url is None:
        return str(ctx.author.avatar.url)


async def process_minecraft(self, b: BytesIO) -> BytesIO:
    minecraft_array = np.array(list(self.bot.minecraft_blocks.keys()))
    np.expand_dims(minecraft_array, axis=-1)
    image = Im.open(b)
    image = image.convert("RGBA").resize((64, 64))
    with Im.new("RGBA", (image.width * 16, image.height * 16)) as final_image:
        arr = np.asarray(image)
        np.expand_dims(arr, axis=-1)
        for y, r in enumerate(arr):
            for x, c in enumerate(r):
                difference = np.sqrt(
                    np.sum((minecraft_array - c) ** 2, axis=1))
                where = np.where(difference == np.amin(difference))
                to_paste = self.bot.minecraft_blocks[tuple(
                    minecraft_array[where][0])]
                final_image.paste(to_paste, (x * 16, y * 16), to_paste)
    buffer = BytesIO()
    final_image.save(buffer, "PNG")
    buffer.seek(0)
    return buffer

async def create_minecraft_blocks(self):
    for _file in os.listdir("assets/minecraft_blocks"):
        async with aiofile.async_open("assets/minecraft_blocks/" + _file, "rb") as afp:
            b = await afp.read()
            await self.resize_and_save_minecraft_blocks(BytesIO(b))

async def resize_and_save_minecraft_blocks(self, b):
    try:
        with Image.open(b) as image:
            image = image.convert("RGBA")
            self.bot.minecraft_blocks[image.resize(
                (1, 1)).getdata()[0]] = image
    except UnidentifiedImageError:
        pass