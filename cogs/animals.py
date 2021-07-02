import discord
from discord.ext import commands

from utils.http import geturljson


class Animals(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.command(name='dog', description="Shows a random dog.", aliases=['dogs'])
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def _dog(self, ctx) -> None:
        async with ctx.typing():
            data = await geturljson("https://some-random-api.ml/img/dog")

        embed = discord.Embed(title=":dog: Here is your dog!",
                              color=discord.Color.dark_green())
        embed.set_image(url=data['link'])
        embed.set_footer(text="Powered by https://some-random-api.ml/")

        await ctx.reply(embed=embed)

    @commands.command(name='cat', description="Shows a random cat.", aliases=['cats'])
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def _cat(self, ctx) -> None:
        async with ctx.typing():
            data = await geturljson("https://some-random-api.ml/img/cat")

        embed = discord.Embed(title=":cat: Here is your cat!",
                              color=discord.Color.dark_green())
        embed.set_image(url=data['link'])
        embed.set_footer(text="Powered by https://some-random-api.ml/")

        await ctx.reply(embed=embed)

    @commands.command(name='panda', description="Shows a random panda.", aliases=['pandas'])
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def _panda(self, ctx) -> None:
        async with ctx.typing():
            data = await geturljson("https://some-random-api.ml/img/panda")

        embed = discord.Embed(title=":panda_face: Here is your panda!",
                              color=discord.Color.dark_green())
        embed.set_image(url=data['link'])
        embed.set_footer(text="Powered by https://some-random-api.ml/")

        await ctx.reply(embed=embed)

    @commands.command(name='bird', description="Shows a random bird.", aliases=['birds'])
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def _bird(self, ctx) -> None:
        async with ctx.typing():
            data = await geturljson("https://some-random-api.ml/img/birb")

        embed = discord.Embed(title=":bird: Here is your bird!",
                              color=discord.Color.dark_green())
        embed.set_image(url=data['link'])
        embed.set_footer(text="Powered by https://some-random-api.ml/")

        await ctx.reply(embed=embed)

    @commands.command(name='fox', description="Shows a random fox.", aliases=['foxes'])
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def _fox(self, ctx) -> None:
        async with ctx.typing():
            data = await geturljson("https://some-random-api.ml/img/fox")

        embed = discord.Embed(title=":fox: Here is your fox!",
                              color=discord.Color.dark_green())
        embed.set_image(url=data['link'])
        embed.set_footer(text="Powered by https://some-random-api.ml/")

        await ctx.reply(embed=embed)

    @commands.command(name='koala', description="Shows a random koala.", aliases=['koalas'])
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def _koala(self, ctx) -> None:
        async with ctx.typing():
            data = await geturljson("https://some-random-api.ml/img/koala")

        embed = discord.Embed(title=":koala: Here is your koala!",
                              color=discord.Color.dark_green())
        embed.set_image(url=data['link'])
        embed.set_footer(text="Powered by https://some-random-api.ml/")

        await ctx.reply(embed=embed)


def setup(bot) -> None:
    bot.add_cog(Animals(bot))