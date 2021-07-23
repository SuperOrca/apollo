from random import choice, randint

import discord
from discord.ext import commands

from utils.context import ApolloContext

_8ball_responses = [
    "It is certain",
    "It is decidedly so",
    "Without a doubt",
    "Yes, definitely",
    "You may rely on it",
    "As I see it, yes",
    "Most likely",
    "Outlook good",
    "Yes",
    "Signs point to yes",
    "Reply hazy try again",
    "Ask again later",
    "Better not tell you now",
    "Cannot predict now",
    "Concentrate and ask again",
    "Don't count on it",
    "My reply is no",
    "My sources say no",
    "Outlook not so good",
    "Very doubtful"
]


class Fun(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot
        self._cd_type = commands.BucketType.user
        self._cd = commands.CooldownMapping.from_cooldown(
            1, 1.5, self._cd_type)

    async def cog_check(self, ctx: ApolloContext):
        bucket = self._cd.get_bucket(ctx.message)
        retry_after = bucket.update_rate_limit()
        if retry_after:
            raise commands.CommandOnCooldown(
                self._cd, retry_after, self._cd_type)
        else:
            return True

    @commands.command(name='8ball', description="Answers a yes/no question.", usage="8ball <question>")
    async def _8ball(self, ctx: ApolloContext, *, question: str) -> None:
        await ctx.reply(embed=discord.Embed(description=f"`Q:` {question}\n`A:` {choice(_8ball_responses)}",
                                            color=discord.Color.purple()))

    @commands.command(name='pp', description="Shows pp size of member.", usage="pp [member]")
    async def _pp(self, ctx: ApolloContext, member: commands.MemberConverter = None):
        member = member or ctx.author
        await ctx.reply(embed=discord.Embed(title=f"{member.name}'s pp size",
                                            description=f"8{'=' * randint(1, 10)}D", color=discord.Color.purple()))

    @commands.command(name='gayrate', description="Shows gay of member.", usage="gayrate [member]")
    async def _gayrate(self, ctx: ApolloContext, member: commands.MemberConverter = None):
        member = member or ctx.author
        await ctx.reply(embed=discord.Embed(description=f":rainbow: **{member.name}** is {randint(1, 100)}% gay",
                                            color=discord.Color.purple()))

    @commands.command(name='roast', description="what u think it does", usage="roast [member]")
    async def _roast(self, ctx: ApolloContext, member: commands.MemberConverter = None):
        member = member or ctx.author
        await ctx.reply(f"**{member.name},** " + await self.bot.dagpi.roast())


def setup(bot) -> None:
    bot.add_cog(Fun(bot))
