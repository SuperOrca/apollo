from discord.ext import commands

from utils.context import Context
from utils.reddit import getpost


class Reddit(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.command(name='meme', description="Shows a random meme.", aliases=['memes'])
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def _meme(self, ctx: Context) -> None:
        await (await getpost(self.bot, ctx.channel, 'memes')).start(ctx)

    @commands.command(name='reddit', description="Shows a random image from a subreddit.", aliases=['r'],
                      usage="reddit <subreddit>")
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def _reddit(self, ctx: Context, subreddit) -> None:
        await (await getpost(self.bot, ctx.channel, subreddit)).start(ctx)


def setup(bot) -> None:
    bot.add_cog(Reddit(bot))
