from discord.ext import commands

from utils.context import ApolloContext


class Animals(commands.Cog):
	def __init__(self, bot) -> None:
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

	@commands.command(name='dog', description="Shows a random dog.", aliases=['dogs'])
	async def _dog(self, ctx: ApolloContext) -> None:
		data = await (await self.bot.session.get("https://some-random-api.ml/img/dog")).json()

		await ctx.reply(data['link'], can_delete=True)

	@commands.command(name='cat', description="Shows a random cat.", aliases=['cats'])
	async def _cat(self, ctx: ApolloContext) -> None:
		data = await (await self.bot.session.get("https://some-random-api.ml/img/cat")).json()

		await ctx.reply(data['link'], can_delete=True)

	@commands.command(name='panda', description="Shows a random panda.", aliases=['pandas'])
	async def _panda(self, ctx: ApolloContext) -> None:
		data = await (await self.bot.session.get("https://some-random-api.ml/img/panda")).json()

		await ctx.reply(data['link'], can_delete=True)

	@commands.command(name='bird', description="Shows a random bird.", aliases=['birds'])
	async def _bird(self, ctx: ApolloContext) -> None:
		data = await (await self.bot.session.get("https://some-random-api.ml/img/birb")).json()

		await ctx.reply(data['link'], can_delete=True)

	@commands.command(name='fox', description="Shows a random fox.", aliases=['foxes'])
	async def _fox(self, ctx: ApolloContext) -> None:
		data = await (await self.bot.session.get("https://some-random-api.ml/img/fox")).json()

		await ctx.reply(data['link'], can_delete=True)

	@commands.command(name='koala', description="Shows a random koala.", aliases=['koalas'])
	async def _koala(self, ctx: ApolloContext) -> None:
		data = await (await self.bot.session.get("https://some-random-api.ml/img/koala")).json()

		await ctx.reply(data['link'], can_delete=True)


def setup(bot) -> None:
	bot.add_cog(Animals(bot))
