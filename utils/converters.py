from discord.ext import commands

from .context import ApolloContext


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
