from io import BytesIO
from bot import Apollo
from discord.ext import commands


import yarl

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

    async def to_blob(self, ctx: ApolloContext, url: str) -> BytesIO:
        response = await ctx.bot.session.get(url)
        return BytesIO(await response.read())

    async def convert(self, ctx: ApolloContext, argument: str) -> BytesIO:

        try:
            member = await commands.MemberConverter().convert(ctx=ctx, argument=str(argument))
        except commands.BadArgument:
            pass
        else:
            await ctx.reply(f'Editing the avatar of `{member}`. If this is a mistake please specify the user/image you would like to edit before any extra arguments.')
            return member.avatar.url

        if (check := yarl.URL(argument)) and check.scheme and check.host:
            return argument

        try:
            emoji = await commands.EmojiConverter().convert(ctx=ctx, argument=str(argument))
        except commands.EmojiNotFound:
            pass
        else:
            return str(emoji.url)

        try:
            partial_emoji = await commands.PartialEmojiConverter().convert(ctx=ctx, argument=str(argument))
        except commands.PartialEmojiConversionFailure:
            pass
        else:
            return str(partial_emoji.url)

        url = f'https://twemoji.maxcdn.com/v/latest/72x72/{ord(argument[0]):x}.png'
        async with ctx.bot.session.get(url) as response:
            if response.status == 200:
                return url

        raise commands.ConversionError(self, original=argument)
