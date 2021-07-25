import discord
from discord.ext import commands

from typing import Union

from .context import ApolloContext
from .image import imageToBytes


class PrefixConverter(commands.clean_content):
    async def convert(self, ctx: ApolloContext, argument: str) -> str:
        self.escape_markdown = True

        if not (argument := (await super().convert(ctx=ctx, argument=argument)).strip()):
            raise commands.BadArgument

        if '`' in argument:
            raise commands.BadArgument(
                'Your prefix can not contain backtick characters.')
        if len(argument) > 15:
            raise commands.BadArgument(
                'Your prefix can not be more than 15 characters.')

        return argument


class ImageConverter(commands.Converter):
    async def convert(self, ctx: ApolloContext, image: Union[discord.Member, discord.Emoji, discord.PartialEmoji, None, str] = None):
        return imageToBytes(ctx, image)
