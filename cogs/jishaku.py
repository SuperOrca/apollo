import discord
from discord.ext import commands
import sys
import math
from typing import Optional
from jishaku.cog import STANDARD_FEATURES, OPTIONAL_FEATURES
from jishaku.features.baseclass import Feature
from jishaku.modules import package_version
import psutil
from utils.metrics import Embed


def natural_size(size_in_bytes: int):
	"""
	Converts a number of bytes to an appropriately-scaled unit
	E.g.:
			1024 -> 1.00 KiB
			12345678 -> 11.77 MiB
	"""
	units = ('B', 'KiB', 'MiB', 'GiB', 'TiB', 'PiB', 'EiB', 'ZiB', 'YiB')

	power = int(math.log(size_in_bytes, 1024))

	return f"{size_in_bytes / (1024 ** power):.2f} {units[power]}"


class Jishaku(*OPTIONAL_FEATURES, *STANDARD_FEATURES):
	@Feature.Command(name="jishaku", aliases=["jsk"], invoke_without_command=True, ignore_extra=False, hidden=True)
	async def jsk(self, ctx: commands.Context):  # pylint: disable=too-many-branches
		summary = [
			f"Jishaku v{package_version('jishaku')}, discord.py `{package_version('discord.py')}`, "
			f"`Python {sys.version}` on `{sys.platform}`".replace(
				"\n", ""),
			f"Module was loaded <t:{self.load_time.timestamp():.0f}:R>, "
			f"cog was loaded <t:{self.start_time.timestamp():.0f}:R>.",
			""
		]

		if psutil:
			try:
				proc = psutil.Process()

				with proc.oneshot():
					try:
						mem = proc.memory_full_info()
						summary.append(f"Using {natural_size(mem.rss)} physical memory and "
									   f"{natural_size(mem.vms)} virtual memory, "
									   f"{natural_size(mem.uss)} of which unique to this process.")
					except psutil.AccessDenied:
						pass

					try:
						name = proc.name()
						pid = proc.pid
						thread_count = proc.num_threads()

						summary.append(
							f"Running on PID {pid} (`{name}`) with {thread_count} thread(s).")
					except psutil.AccessDenied:
						pass

					summary.append("")  # blank line
			except psutil.AccessDenied:
				summary.append(
					"psutil is installed, but this process does not have high enough access rights "
					"to query process information."
				)
				summary.append("")  # blank line

		cache_summary = f"{len(self.bot.guilds)} guild(s) and {len(self.bot.users)} user(s)"

		if isinstance(self.bot, discord.AutoShardedClient):
			if len(self.bot.shards) > 20:
				summary.append(
					f"This bot is automatically sharded ({len(self.bot.shards)} shards of {self.bot.shard_count})"
					f" and can see {cache_summary}."
				)
			else:
				shard_ids = ', '.join(str(i) for i in self.bot.shards.keys())
				summary.append(
					f"This bot is automatically sharded (Shards {shard_ids} of {self.bot.shard_count})"
					f" and can see {cache_summary}."
				)
		elif self.bot.shard_count:
			summary.append(
				f"This bot is manually sharded (Shard {self.bot.shard_id} of {self.bot.shard_count})"
				f" and can see {cache_summary}."
			)
		else:
			summary.append(
				f"This bot is not sharded and can see {cache_summary}.")

		if self.bot._connection.max_messages:
			message_cache = f"Message cache capped at {self.bot._connection.max_messages}"
		else:
			message_cache = "Message cache is disabled"

		if discord.version_info >= (1, 5, 0):
			presence_intent = f"presence intent is {'enabled' if self.bot.intents.presences else 'disabled'}"
			members_intent = f"members intent is {'enabled' if self.bot.intents.members else 'disabled'}"

			summary.append(
				f"{message_cache}, {presence_intent} and {members_intent}.")
		else:
			guild_subscriptions = f"guild subscriptions are {'enabled' if self.bot._connection.guild_subscriptions else 'disabled'}"

			summary.append(f"{message_cache} and {guild_subscriptions}.")

		summary.append(
			f"Average websocket latency: {round(self.bot.latency * 1000, 2)}ms")

		await ctx.send(embed=Embed(description="\n".join(summary)))

	@Feature.Command(parent="jsk", name="grammar")
	async def jsk_grammar(self, ctx: commands.Context, *, text: str):
		await ctx.send(
			''.join(char.upper() if index % 2 == 0 else char.lower() for index, char in enumerate(text, start=1)))

	@Feature.Command(parent="jsk", name="blacklist")
	async def jsk_blacklist(self, ctx: commands.Context, mode: str, user: Optional[commands.UserConverter] = None):
		if mode == "list":
			await ctx.send('Blacklist: ' + ', '.join(f"`{self.bot.get_user(u)}`" for u in self.bot.blacklist))
		elif mode == "add":
			self.bot.blacklist.append(user.id)
			await ctx.send(f'Added `{user}` to the blacklist.')
		elif mode == "remove":
			self.bot.blacklist.remove(user.id)
			await ctx.send(f'Removed `{user}` from the blacklist.')


def setup(bot):
	bot.add_cog(Jishaku(bot))
