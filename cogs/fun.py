import asyncio
from config import EIGHT_BALL
from random import choice, randint
from typing import Optional

from discord.ext import commands

from utils.context import ApolloContext
from utils.metrics import Embed

class Fun(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot
        self._cd_type = commands.BucketType.user
        self._cd = commands.CooldownMapping.from_cooldown(
            1, 2., self._cd_type)

    async def cog_check(self, ctx: ApolloContext):
        bucket = self._cd.get_bucket(ctx.message)
        retry_after = bucket.update_rate_limit()
        if retry_after:
            raise commands.CommandOnCooldown(
                self._cd, retry_after, self._cd_type)
        else:
            return True

    @commands.command(name='8ball', description="Answers a yes/no question.", usage="<question>")
    async def _8ball(self, ctx: ApolloContext, *, question: commands.clean_content) -> None:
        await ctx.reply(embed=Embed(description=f"**Question**: {question}\n**Answer**: {choice(EIGHT_BALL)}"))

    @commands.command(name='pp', description="Shows pp size of member.", usage="[member]")
    async def _pp(self, ctx: ApolloContext, member: Optional[commands.UserConverter] = None):
        member = member or ctx.author
        await ctx.reply(embed=Embed(title=f"{member.name}'s pp size",
                                    description=f"8{'=' * randint(1, 10)}D"))

    @commands.command(name='gayrate', description="Shows gay of member.", usage="[member]")
    async def _gayrate(self, ctx: ApolloContext, member: Optional[commands.UserConverter] = None):
        member = member or ctx.author
        await ctx.reply(embed=Embed(description=f":rainbow: **{member.name}** is {randint(1, 100)}% gay"))

    @commands.command(name='roast', description="what u think it does", usage="[member]")
    async def _roast(self, ctx: ApolloContext, member: Optional[commands.UserConverter] = None):
        member = member or ctx.author
        await ctx.reply(f"**{member.name},** " + await self.bot.dagpi.roast())

    @commands.command(name='fact', description="Shows a random fact.")
    async def _fact(self, ctx: ApolloContext):
        fact = await self.bot.dagpi.fact()
        await ctx.reply(embed=Embed(description=fact))

    @commands.command(name='yomama', description="Shows a random yomama joke.")
    async def _yomama(self, ctx: ApolloContext):
        yomama = await self.bot.dagpi.yomama()
        await ctx.reply(embed=Embed(description=yomama))

    @commands.command(name='joke', description="Shows a random yomama joke.")
    async def _joke(self, ctx: ApolloContext):
        joke = await self.bot.dagpi.joke()
        await ctx.reply(embed=Embed(description=joke))

    @commands.command(name='wtp', description="Whose that pokemon!")
    @commands.cooldown(1, 15, commands.BucketType.user)
    async def _wtp(self, ctx: ApolloContext):
        wtp = await self.bot.dagpi.wtp()
        embed = Embed(title='Whose that Pokemon?',
                      description=f"**Abilties:** {', '.join(wtp.abilities)}")
        embed.set_image(url=wtp.question)
        await ctx.send(embed=embed)
        try:
            message = await self.bot.wait_for('message', timeout=10, check=lambda
                m: m.channel == ctx.channel and m.content.lower() == wtp.name.lower())
            embed = Embed(
                title=f"{message.author.name} got the Pokemon!", description=f"It was a **{wtp.name}**.")
            embed.set_image(url=wtp.answer)
            await ctx.send(embed=embed)
        except asyncio.TimeoutError:
            embed = Embed(
                title=f"Nobody got the Pokemon!", description=f"It was a **{wtp.name}**.")
            embed.set_image(url=wtp.answer)
            await ctx.send(embed=embed)


def setup(bot) -> None:
    bot.add_cog(Fun(bot))
