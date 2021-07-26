from io import BytesIO
from bot import ApolloContext
from discord.ext import commands


import yarl
import re

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

        return argument


class ImageConverter(commands.Converter):

    async def to_blob(self, ctx: ApolloContext, url: str) -> BytesIO:
        response = await ctx.bot.session.get(url)
        if response.status == 200 and 'image/' in response.content_type:
            blob = BytesIO(await response.read())
            blob.seek(0)
            return blob
        raise commands.BadArgument("URL is not image.")

    async def convert(self, ctx: ApolloContext, argument: str) -> BytesIO:

        try:
            member = await commands.MemberConverter().convert(ctx=ctx, argument=str(argument))
        except commands.BadArgument:
            pass
        else:
            return await self.to_blob(ctx, member.avatar.url)

        if (check := yarl.URL(argument)) and check.scheme and check.host:
            return await self.to_blob(ctx, argument)

        try:
            emoji = await commands.EmojiConverter().convert(ctx=ctx, argument=str(argument))
        except commands.EmojiNotFound:
            pass
        else:
            return await self.to_blob(ctx, str(emoji.url))

        try:
            partial_emoji = await commands.PartialEmojiConverter().convert(ctx=ctx, argument=str(argument))
        except commands.PartialEmojiConversionFailure:
            pass
        else:
            return await self.to_blob(ctx, str(partial_emoji.url))

        url = f'https://twemoji.maxcdn.com/v/latest/72x72/{ord(argument[0]):x}.png'
        async with ctx.bot.session.get(url) as response:
            if response.status == 200:
                return await self.to_blob(ctx, url)

        pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*(),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
        if re.match(pattern, argument):
            return await self.to_blob(ctx, argument)

        raise commands.ConversionError(self, original=argument)
