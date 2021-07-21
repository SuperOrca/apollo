from discord.ext import commands
import discord
from random import choice, randint
from utils.economy import Account
from utils.context import ApolloContext


class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(help="Get the balance of a member.", aliases=['bal'])
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def balance(self, ctx: ApolloContext, member: commands.MemberConverter = None):
        member = member or ctx.author
        acc = await Account.fetch(self.bot, member)
        embed = discord.Embed(
            description=f"Wallet: ${acc.wallet:,}\nBank: ${acc.bank:,}")
        embed.set_author(name=f"{member}'s Account",
                         icon_url=member.avatar_url)
        await ctx.send(embed=embed)

    @commands.command(help="Withdraw money from your bank.")
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def withdraw(self, ctx: ApolloContext, money: int):
        acc = await Account.fetch(self.bot, ctx.author)
        await acc.withdraw(money)
        await ctx.send(f"You withdrew ${money} from your bank.")

    @commands.command(help="Deposit money in your bank.", aliases=['dep'])
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def deposit(self, ctx: ApolloContext, money: int):
        acc = await Account.fetch(self.bot, ctx.author)
        await acc.deposit(money)
        await ctx.send(f"You desposited ${money} in your bank.")

    @commands.command(help="Beg for a bit of money.")
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def beg(self, ctx: ApolloContext):
        if choice([True, False]):
            money = randint(4, 12)
            acc = await Account.fetch(self.bot, ctx.author)
            acc.wallet += money
            await acc.commit()
            await ctx.send(f"Here you go! +${money}")
        else:
            await ctx.send("Sorry, I have no cash today. :(")


def setup(bot):
    bot.add_cog(Economy(bot))
