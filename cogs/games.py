from discord.ext import commands

from utils.context import ApolloContext
from utils.games.typeracer import TypeRacer


class Games(commands.Cog):
	def __init__(self, bot) -> None:
		self.bot = bot
		self._cd_type = commands.BucketType.user
		self._cd = commands.CooldownMapping.from_cooldown(1, 90, self._cd_type)

	async def cog_check(self, ctx: ApolloContext):
		bucket = self._cd.get_bucket(ctx.message)
		retry_after = bucket.update_rate_limit()
		if retry_after:
			raise commands.CommandOnCooldown(
				self._cd, retry_after, self._cd_type)
		else:
			return True

	@commands.command(name='typeracer', description="Typeracer game!")
	async def _typeracer(self, ctx: ApolloContext) -> None:
		await TypeRacer().start(ctx, show_author=False, path_to_text_font='assets/fira.ttf', timeout=60.)


def setup(bot) -> None:
	bot.add_cog(Games(bot))
