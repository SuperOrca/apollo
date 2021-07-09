import discord
from discord.ext import commands


class Error(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context, error) -> None:
        if hasattr(ctx.command, 'on_error'):
            return

        ignored = (commands.CommandNotFound,
                   commands.DisabledCommand, commands.NoPrivateMessage)

        if isinstance(error, ignored):
            return

        if isinstance(error, commands.MissingRequiredArgument):
            error = f"You are missing the required `{str(error).split()[0].upper()}` argument."

        self.bot.log.error(f"{ctx.command} -> {error}")
        await ctx.reply(embed=discord.Embed(description=error, color=discord.Color.red()))


def setup(bot) -> None:
    bot.add_cog(Error(bot))
