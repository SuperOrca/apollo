from discord.ext import commands

from utils.context import ApolloContext
from utils.reddit import getpost


class Reddit(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot
        self._cd_type = commands.BucketType.user
        self._cd = commands.CooldownMapping.from_cooldown(
            1, 10., self._cd_type)

    async def cog_check(self, ctx: ApolloContext):
        bucket = self._cd.get_bucket(ctx.message)
        retry_after = bucket.update_rate_limit()
        if retry_after:
            raise commands.CommandOnCooldown(
                self._cd, retry_after, self._cd_type)
        else:
            return True

    @commands.command(name='meme', description="Shows a random meme.", aliases=['memes'])
    async def _meme(self, ctx: ApolloContext) -> None:
        view = await getpost(self.bot, ctx.channel, 'memes')
        await view.start(ctx)

    @commands.command(name='reddit', description="Shows a random image from a subreddit.", aliases=['r'],
                      usage="<subreddit>")
    async def _reddit(self, ctx: ApolloContext, subreddit) -> None:
        view = await getpost(self.bot, ctx.channel, subreddit)
        await view.start(ctx)


def setup(bot) -> None:
    bot.add_cog(Reddit(bot))
