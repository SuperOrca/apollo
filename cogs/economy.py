from random import choice, randint
from typing import Optional

import discord
from discord.ext import commands

from utils.context import ApolloContext
from utils.economy import Account


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

	@commands.command(description="Get the balance of a member.", aliases=['bal'], usage="[member]")
	@commands.cooldown(1, 2, commands.BucketType.user)
	async def balance(self, ctx: ApolloContext, member: Optional[commands.UserConverter] = None):
		member = member or ctx.author
		acc = await Account.fetch(self.bot, member)
		embed = discord.Embed(color=discord.Color.green(), description=f"""
		**Wallet**: ${acc.wallet:,}
		**Bank**: ${acc.bank:,}
		""")
		embed.set_author(name=f"{member}'s Account", icon_url=member.avatar.url)
		await ctx.reply(embed=embed)

	@commands.command(description="Withdraw money from your bank.", usage="<money>")
	async def withdraw(self, ctx: ApolloContext, money: int):
		acc = await Account.fetch(self.bot, ctx.author)
		await acc.withdraw(money)
		await ctx.reply(
			embed=discord.Embed(description=f"You withdrew `${money}` from your bank.", color=discord.Color.green()))

	@commands.command(description="Deposit money in your bank.", aliases=['dep'], usage="<money>")
	async def deposit(self, ctx: ApolloContext, money: int):
		acc = await Account.fetch(self.bot, ctx.author)
		await acc.deposit(money)
		await ctx.reply(
			embed=discord.Embed(description=f"You desposited `${money}` in your bank.", color=discord.Color.green()))

	@commands.command(name='beg', description="Beg for a bit of money.")
	@commands.cooldown(1, 15, commands.BucketType.user)
	async def _beg(self, ctx: ApolloContext):
		if choice([True, False]):
			money = randint(4, 12)
			acc = await Account.fetch(self.bot, ctx.author)
			acc.wallet += money
			await acc.commit()
			await ctx.reply(embed=discord.Embed(description=f"Here you go! `+${money}`", color=discord.Color.green()))
		else:
			await ctx.reply(
				embed=discord.Embed(description="Sorry, I have no cash today. :(", color=discord.Color.green()))

	# TODO more commands


def setup(bot):
	bot.add_cog(Economy(bot))
