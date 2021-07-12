from random import choice, randint

import discord
from discord.ext import commands

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

    @commands.command(name='8ball', description="Answers a yes/no question.", usage="8ball <question>")
    async def _8ball(self, ctx: commands.Context, *, question: str) -> None:
        await ctx.reply(embed=discord.Embed(description=f"`Q:` {question}\n`A:` {choice(_8ball_responses)}",
                                            color=discord.Color.purple()))

    @commands.command(name='pp', description="Shows pp size of member.", usage="pp [member]")
    async def _pp(self, ctx: commands.Context, member: commands.MemberConverter = None):
        member = member or ctx.author
        await ctx.reply(embed=discord.Embed(title=f"{member.name}'s pp size",
                                            description=f"8{'=' * randint(1, 10)}D", color=discord.Color.purple()))


def setup(bot) -> None:
    bot.add_cog(Fun(bot))
