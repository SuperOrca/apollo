from io import BytesIO
import discord
from discord.ext import commands
import twemoji_parser as twemoji


import re
from typing import Union

from .context import ApolloContext
from .metrics import isImage


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

        url = argument


class ImageConverter(commands.Converter):
    async def convert(self, ctx: ApolloContext, url: Union[discord.Member, discord.Emoji, discord.PartialEmoji, None, str] = None) -> BytesIO:
        if isinstance(url, str):
            url = await twemoji.emoji_to_url(url)

        if ctx.message.reference:
            ref = ctx.message.reference.resolved
            if ref.embeds:
                if ref.embeds[0].image.url != discord.Embed.Empty and isImage(
                        ref.embeds[0].image.url
                ):
                    url = ref.embeds[0].image.url

                if ref.embeds[0].thumbnail.url != discord.Embed.Empty and isImage(
                        ref.embeds[0].thumbnail.url
                ):
                    url = ref.embeds[0].thumbnail.url

            elif ref.attachments:
                url = ref.attachments[0].url or ref.attachments[0].proxy_url
                if isImage(url):
                    url = url

        if isinstance(url, discord.Member):
            url = str(url.avatar.url)
        elif isinstance(url, str):
            if re.search(
                    r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*(),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+",
                    url,
            ) and isImage(url):
                url = url

        if isinstance(url, (discord.Emoji, discord.PartialEmoji)):
            url = url.url

        if ctx.message.attachments:

            url = ctx.message.attachments[0].url or ctx.message.attachments[0].proxy_url

            if isImage(url):
                url = ctx.message.attachments[0].proxy_url or ctx.message.attachments[0].url

            elif isinstance(url, discord.Member):
                url = str(url.avatar.url)
            else:
                url = str(ctx.author.avatar.url)

        if url is None:
            url = str(ctx.author.avatar.url)

        print(url)
        response = await ctx.bot.session.get(url)
        blob = BytesIO(await response.read())
        blob.seek(0)
        return blob
