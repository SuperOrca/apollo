from discord.ext import commands

import statcord


class StatcordPost(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot
        self.key = "statcord.com-opCEcmtQbIAQtl3qtHej"
        self.api = statcord.Client(self.bot, self.key)
        self.api.start_loop()

    @commands.Cog.listener()
    async def on_command(self, ctx) -> None:
        self.api.command_run(ctx)


def setup(bot) -> None:
    bot.add_cog(StatcordPost(bot))
