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
            raise commands.UserInputError

        if '`' in argument:
            raise commands.UserInputError(
                'Your prefix can not contain backtick characters.')
        if len(argument) > 15:
            raise commands.UserInputError(
                'Your prefix can not be more than 15 characters.')

        return argument

class AssetResponse:
    def __init__(self, _url, _format):
        self.url = _url
        self.format = _format

    def is_animated(self):
        return self.format == 'image/gif'

    @classmethod
    async def from_url(cls, _url, _format=None, _bot=None):
        if not _format and _bot:
            response = await _bot.session.get(_url)
            _format = response.content_type
        return cls(_url, _format)


class ImageConverter(commands.Converter):
    """A converter for getting a url from an argument."""

    async def convert(self, ctx: ApolloContext, argument: str) -> BytesIO:

        try:
            member = await commands.MemberConverter().convert(ctx=ctx, argument=str(argument))
        except commands.BadArgument:
            pass
        else:
            return await AssetResponse(member.avatar.url, _bot=ctx.bot)

        try:
            emoji = await commands.EmojiConverter().convert(ctx=ctx, argument=str(argument))
        except commands.EmojiNotFound:
            pass
        else:
            return await AssetResponse(emoji.url, _bot=ctx.bot)

        try:
            partial_emoji = await commands.PartialEmojiConverter().convert(ctx=ctx, argument=str(argument))
        except commands.PartialEmojiConversionFailure:
            pass
        else:
            return await AssetResponse(str(partial_emoji.url), _bot=ctx.bot)

        url = f'https://twemoji.maxcdn.com/v/latest/72x72/{ord(argument[0]):x}.png'
        async with ctx.bot.session.get(url) as response:
            if response.status == 200 and 'image/' in response.content_type:
                return await AssetResponse(url, _format=response.content_type)

        if (check := yarl.URL(argument)) and check.scheme and check.host:
            async with ctx.bot.session.get(argument) as response:
                if response.status == 200 and 'image/' in response.content_type:
                    return await AssetResponse.from_url(argument, _format=response.content_type)

        raise commands.ConversionError(self, original=argument)
