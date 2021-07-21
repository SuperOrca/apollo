from discord.ext import commands
import discord
from random import choice, randint
from utils.economy import Account
from utils.context import ApolloContext


class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._cd_type = commands.BucketType.user
        self._cd = commands.CooldownMapping.from_cooldown(
            1, 2.5, self._cd_type)

    async def cog_check(self, ctx: ApolloContext):
        bucket = self._cd.get_bucket(ctx.message)
        retry_after = bucket.update_rate_limit()
        if retry_after:
            raise commands.CommandOnCooldown(
                self._cd, retry_after, self._cd_type)
        else:
            return True

    @commands.command(description="Get the balance of a member.", aliases=['bal'], usage="balance [member]")
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def balance(self, ctx: ApolloContext, member: commands.MemberConverter = None):
        member = member or ctx.author
        acc = await Account.fetch(self.bot, member)
        embed = discord.Embed(color=discord.Color.green())
        embed.add_field(name="Wallet", description=f"${acc.wallet:,}", inline=True)
        embed.add_field(name="Bank", description=f"${acc.bank:,}", inline=True)
        embed.set_author(name=f"{member}'s Account", icon_url=member.avatar.url)
        await ctx.reply(embed=embed)

    @commands.command(description="Withdraw money from your bank.", usage="withdraw <money>")
    async def withdraw(self, ctx: ApolloContext, money: int):
        acc = await Account.fetch(self.bot, ctx.author)
        await acc.withdraw(money)
        await ctx.reply(embed=discord.Embed(description=f"You withdrew ${money} from your bank.", color=discord.Color.green()))

    @commands.command(description="Deposit money in your bank.", aliases=['dep'], usage="deposit <money>")
    async def deposit(self, ctx: ApolloContext, money: int):
        acc = await Account.fetch(self.bot, ctx.author)
        await acc.deposit(money)
        await ctx.reply(embed=discord.Embed(description=f"You desposited ${money} in your bank.", color=discord.Color.green()))

    @commands.command(name='beg', description="Beg for a bit of money.")
    @commands.cooldown(1, 15, commands.BucketType.user)
    async def _beg(self, ctx: ApolloContext):
        if choice([True, False]):
            money = randint(4, 12)
            acc = await Account.fetch(self.bot, ctx.author)
            acc.wallet += money
            await acc.commit()
            await ctx.reply(f"Here you go! +${money}")
        else:
            await ctx.reply(embed=discord.Embed(description="Sorry, I have no cash today. :(", color=discord.Color.green()))


def setup(bot):
    bot.add_cog(Economy(bot))
