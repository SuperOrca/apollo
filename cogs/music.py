import datetime
import math
from utils.music import Song, VoiceState, YTDLSource

import discord
import youtube_dl
from discord.ext import commands

from utils.context import ApolloContext
from utils.metrics import Embed
from utils.paginator import EmbedPaginator

# Silence useless bug reports messages
youtube_dl.utils.bug_reports_message = lambda: ''


class Music(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.voice_states = {}
		self._cd_type = commands.BucketType.user
		self._cd = commands.CooldownMapping.from_cooldown(
			1, 3, self._cd_type)

	async def cog_check(self, ctx: ApolloContext):
		bucket = self._cd.get_bucket(ctx.message)
		retry_after = bucket.update_rate_limit()
		if retry_after:
			raise commands.CommandOnCooldown(
				self._cd, retry_after, self._cd_type)
		else:
			return True

	def get_voice_state(self, guild: discord.Guild):
		state = self.voice_states.get(guild.id)
		if not state:
			state = VoiceState(self.bot, guild)
			self.voice_states[guild.id] = state

		return state

	def cog_unload(self):
		for state in self.voice_states.values():
			self.bot.loop.create_task(state.stop())

	async def cog_before_invoke(self, ctx: ApolloContext):
		ctx.voice_state = self.get_voice_state(ctx.guild)

	@commands.command(name='join', description="Joins a voice channel.", aliases=['connect'])
	async def _join(self, ctx: ApolloContext):
		await self.ensure_voice_state(ctx)

		destination = ctx.author.voice.channel
		if ctx.voice_state.voice:
			await ctx.voice_state.voice.move_to(destination)
			return

		ctx.voice_state.voice = await destination.connect()
		await ctx.tick()

	@commands.command(name='leave', description="Clears the queue and leaves the voice channel.",
					  aliases=['disconnect', 'stop', 'dc'])
	async def _leave(self, ctx: ApolloContext):
		await self.ensure_voice_state(ctx)

		if not ctx.voice_state.voice:
			raise commands.UserInputError('Not connected to any voice channel.')

		await ctx.voice_state.stop()
		del self.voice_states[ctx.guild.id]
		await ctx.tick()

	@commands.command(name='now', description="Displays the currently playing song.", aliases=['current', 'playing', 'np'])
	async def _now(self, ctx: ApolloContext):
		await ctx.reply(embed=ctx.voice_state.current.create_embed())

	@commands.command(name='pause', description="Pauses the currently playing song.")
	async def _pause(self, ctx: ApolloContext):
		await self.ensure_voice_state(ctx)

		if ctx.voice_state.is_playing and ctx.voice_state.voice.is_playing():
			ctx.voice_state.voice.pause()
			await ctx.tick()
			return

		raise commands.UserInputError('Player is already paused.')

	@commands.command(name='resume', description="Resumes a currently paused song.", aliases=['unpause'])
	async def _resume(self, ctx: ApolloContext):
		await self.ensure_voice_state(ctx)

		if not ctx.voice_state.is_playing and ctx.voice_state.voice.is_paused():
			ctx.voice_state.voice.resume()
			await ctx.tick()
			return

		raise commands.UserInputError('Player is already playing.')

	@commands.command(name='skip', description="Skip a song.", aliases=['s'])
	async def _skip(self, ctx: ApolloContext):
		await self.ensure_voice_state(ctx)

		if not ctx.voice_state.is_playing:
			raise commands.UserInputError('Not playing any music right now...')

		ctx.voice_state.skip()
		await ctx.tick()

	@commands.command(name='queue', description="Shows the player's queue.", aliases=['q'])
	async def _queue(self, ctx: ApolloContext):
		if len(ctx.voice_state.songs) == 0:
			raise commands.UserInputError('Empty queue.')

		embeds = []
		items_per_page = 10
		pages = math.ceil(len(ctx.voice_state.songs) / items_per_page)

		for page in range(1, (pages + 1)):
			start = (page - 1) * items_per_page
			end = start + items_per_page

			queue = """Now. [{0.source.title}]({0.source.url}) | {0.source.requester.mention}\n\n""".format(ctx.voice_state.current)
			for i, song in enumerate(ctx.voice_state.songs[start:end], start=start):
				queue += '{0}. [{1.source.title}]({1.source.url}) | {1.source.requester.mention}\n'.format(
					i + 1, song)

			embeds.append(Embed(title=f'Queue for {ctx.guild.name}', description=queue + f"""
			**{len(ctx.voice_state.songs)} songs in queue | {str(sum([i.source.duration for i in ctx.voice_state.songs], datetime.timedelta()))} total length**
			""")
					.set_footer(text='Viewing page {}/{}'.format(page, pages)))
		await EmbedPaginator.start(ctx, embeds)

	@commands.command(name='shuffle', description="Shuffles the queue.", aliases=['sh'])
	async def _shuffle(self, ctx: ApolloContext):
		await self.ensure_voice_state(ctx)
		
		if len(ctx.voice_state.songs) == 0:
			raise commands.UserInputError('Empty queue.')

		ctx.voice_state.songs.shuffle()
		await ctx.tick()

	@commands.command(name='remove', description="Removes a song from the queue at a given index.", aliases=['rm'])
	async def _remove(self, ctx: ApolloContext, index: int):
		await self.ensure_voice_state(ctx)

		if len(ctx.voice_state.songs) == 0:
			raise commands.UserInputError('Empty queue.')

		ctx.voice_state.songs.remove(index - 1)
		await ctx.tick()

	@commands.command(name='loop', description="Loops the currently playing song.")
	async def _loop(self, ctx: ApolloContext):
		await self.ensure_voice_state(ctx)
		
		if not ctx.voice_state.is_playing:
			raise commands.UserInputError('Nothing being played at the moment.')

		ctx.voice_state.loop = not ctx.voice_state.loop
		await ctx.tick()

	@commands.command(name='play', description="Plays a song.", aliases=['p'])
	async def _play(self, ctx: ApolloContext, *, search: str):
		await self.ensure_voice_state(ctx)

		if not ctx.voice_state.voice:
			await ctx.invoke(self._join)

		source = await YTDLSource.create_source(ctx, search, loop=self.bot.loop)

		if len(source) > 1:
			if sum([s.raw_duration for s in source]) > 36000:
				raise commands.UserInputError("Playlist duration is greater than 10 hours.")
		else:
			if source[0].raw_duration > 3600:
				raise commands.UserInputError("Song duration is greater than 1 hour.")

		if (len(ctx.voice_state.songs) + len(source)) > 50:
			raise commands.UserInputError("Cannot enqueue more than 99 songs.")

		for s in source:
			song = Song(s)
			await ctx.voice_state.songs.put(song)

		if len(source) > 1:
			await ctx.reply(embed=Embed(description=f"Queued `{len(source)}` songs | {ctx.author.mention}"))
		else:
			await ctx.reply(embed=Embed(description=f"Queued [{source[0].title}]({source[0].url}) | {ctx.author.mention}"))

	@commands.Cog.listener()
	async def on_voice_state_update(self, member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
		if member == self.bot.user:
			if after.channel is None:
				voice_state = self.voice_states.get(member.guild.id)
				if voice_state:
					await voice_state.stop()
					del self.voice_states[member.guild.id]

	async def ensure_voice_state(self, ctx: ApolloContext):
		if not ctx.author.voice or not ctx.author.voice.channel:
			raise commands.UserInputError('You are not connected to any voice channel.')

		if ctx.voice_client:
			if ctx.voice_client.channel != ctx.author.voice.channel:
				raise commands.UserInputError('The bot is already in a voice channel.')

def setup(bot):
	bot.add_cog(Music(bot))
