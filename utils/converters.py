import re
from io import BytesIO

import yarl
from discord.ext import commands

from utils.context import ApolloContext


class PrefixConverter(commands.clean_content):
    """A converter for format an argument for use as prefix."""

    async def convert(self, ctx: ApolloContext, argument: str) -> str:
        self.escape_markdown = True

        if not (argument := (await super().convert(ctx=ctx, argument=argument)).strip()):
            raise commands.CommandError

        if '`' in argument:
            raise commands.CommandError(
                'Your prefix can not contain backtick characters.')
        if len(argument) > 15:
            raise commands.CommandError(
                'Your prefix can not be more than 15 characters.')

        return argument


class ImageConverter(commands.Converter):
    """A converter for getting a url from an argument."""

    async def convert(self, ctx: ApolloContext, argument: str) -> BytesIO:

        try:
            member = await commands.MemberConverter().convert(ctx=ctx, argument=str(argument))
        except commands.BadArgument:
            pass
        else:
            return member.avatar.url

        if (check := yarl.URL(argument)) and check.scheme and check.host:
            return argument

        try:
            emoji = await commands.EmojiConverter().convert(ctx=ctx, argument=str(argument))
        except commands.EmojiNotFound:
            pass
        else:
            return emoji.url

        try:
            partial_emoji = await commands.PartialEmojiConverter().convert(ctx=ctx, argument=str(argument))
        except commands.PartialEmojiConversionFailure:
            pass
        else:
            return str(partial_emoji.url)

        url = f'https://twemoji.maxcdn.com/v/latest/72x72/{ord(argument[0]):x}.png'
        async with ctx.bot.session.get(url) as response:
            if response.status == 200 and 'image/' in response.content_type:
                return url

        pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*(),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
        if re.match(pattern, argument):
            async with ctx.bot.session.get(url) as response:
                if response.status == 200 and 'image/' in response.content_type:
                    return url

        raise commands.ConversionError(self, original=argument)
