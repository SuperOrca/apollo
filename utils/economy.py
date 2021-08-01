import discord
from discord.ext import commands


class Account:
	def __init__(self, bot: commands.Bot, member: discord.Member, data: tuple):
		self.bot = bot
		self.member = member
		self.wallet = data[1]
		self.bank = data[2]
		self.bankcap = data[3]
		self.multi = data[4]
		self.daily = data[5]

	async def withdraw(self, money: int):
		if money <= 0:
			raise commands.BadArgument(f"You must withdraw at least `$1`.")
		if self.bank < money:
			raise commands.BadArgument(
				f"You cannot withdraw more than `${self.bank:,}`.")
		self.bank -= money
		self.wallet += money
		await self.commit()

	async def deposit(self, money: int):
		if money <= 0:
			raise commands.BadArgument(f"You must deposit at least `$1`.")
		if self.wallet < money:
			raise commands.BadArgument(
				f"You cannot deposit more than `${self.wallet:,}`.")
		self.wallet -= money
		self.bank += money
		await self.commit()

	async def commit(self):
		await self.bot.db.execute(
			"UPDATE economy SET wallet = :wallet, bank = :bank, bankcap = :bankcap, multi = :multi, daily = :daily",
			values={
				"wallet": self.wallet,
				"bank": self.bank,
				"bankcap": self.bankcap,
				"multi": self.multi,
				"daily": self.daily
			})

	@classmethod
	async def fetch(cls, bot: commands.Bot, member: discord.Member):
		"""A method that fetches the account of a member."""
		if member.bot:
			raise commands.BadArgument(
				"You cannot use this command with a bot.")
		data = await bot.db.fetch_one("SELECT * FROM economy WHERE id = :id", values={"id": member.id})
		if data is None:
			bot.log.info(f"Creating new account for {member} ({member.id}).")
			await bot.db.execute("INSERT INTO economy VALUES (:id, :wallet, :bank, :bankcap, :multi, :daily)", values={
				"id": member.id,
				"wallet": 0,
				"bank": 0,
				"bankcap": 500,
				"multi": 0,
				"daily": None
			})
			data = (member.id, 0, 0, 500, 0, None)
		return cls(bot, member, data)
