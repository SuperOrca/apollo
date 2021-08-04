import discord
import youtube_dl
from discord.ext import commands
from utils.context import ApolloContext
from datetime import timedelta
from typing import Optional
import itertools
import functools
import random
from async_timeout import timeout
import asyncio
from utils.metrics import Embed


class YTDLSource(discord.PCMVolumeTransformer):
	YTDL_OPTIONS = {
		'format': 'bestaudio/best',
		'extractaudio': True,
		'audioformat': 'mp3',
		'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
		'restrictfilenames': True,
		'noplaylist': True,
		'nocheckcertificate': True,
		'ignoreerrors': False,
		'logtostderr': False,
		'quiet': True,
		'no_warnings': True,
		'default_search': 'auto',
		'source_address': '0.0.0.0',
	}

	FFMPEG_OPTIONS = {
		'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
		'options': '-vn',
	}

	ytdl = youtube_dl.YoutubeDL(YTDL_OPTIONS)

	def __init__(self, ctx: ApolloContext, source: discord.FFmpegPCMAudio, *, data: dict, volume: float = 0.5):
		super().__init__(source, volume)

		self.requester = ctx.author
		self.channel = ctx.channel
		self.data = data

		self.uploader = data.get('uploader')
		self.uploader_url = data.get('uploader_url')
		date = data.get('upload_date')
		self.upload_date = date[6:8] + '.' + date[4:6] + '.' + date[0:4]
		self.title = data.get('title')
		self.thumbnail = data.get('thumbnail')
		self.description = data.get('description')
		self.raw_duration = int(data.get('duration'))
		if self.raw_duration == 0:
			raise commands.UserInputError("Cannot enqueue streams.")
		self.duration = timedelta(seconds=self.raw_duration)
		self.formatted_duration = str(self.duration)
		self.tags = data.get('tags')
		self.url = data.get('webpage_url')
		self.views = data.get('view_count')
		self.likes = data.get('like_count')
		self.dislikes = data.get('dislike_count')
		self.stream_url = data.get('url')

	def __str__(self):
		return self.title

	@staticmethod
	async def get_processed_info(cls, search, loop, process=True):
		partial = functools.partial(
			cls.ytdl.extract_info, search, download=False, process=process)
		return await loop.run_in_executor(None, partial)

	@classmethod
	async def create_source(cls, ctx: ApolloContext, search: str, *, loop: Optional[asyncio.BaseEventLoop] = None):
		loop = loop or asyncio.get_event_loop()

		data = await cls.get_processed_info(cls, search, loop, process=False)

		if data is None:
			raise commands.UserInputError(
				'Couldn\'t find anything that matches `{}`'.format(search))

		output = []
		if 'entries' in data:
			entries = []
			for entry in data['entries']:
				if entry:
					entries.append(entry)
			if len(entries) < 1:
				raise commands.UserInputError(
					'Couldn\'t find anything that matches `{}`'.format(search))
			webpage_url = data.get('webpage_url', data.get('url'))
			info = await cls.get_processed_info(cls, webpage_url, loop)
			if info is None:
				raise commands.UserInputError(
					'Couldn\'t fetch `{}`'.format(webpage_url))

			for entry in info['entries']:
				output.append(cls(ctx, discord.FFmpegPCMAudio(
					entry.get('url'), **cls.FFMPEG_OPTIONS), data=entry))
		else:
			webpage_url = data.get('webpage_url', data.get('url'))
			info = await cls.get_processed_info(cls, webpage_url, loop)

			if info is None:
				raise commands.UserInputError(
					'Couldn\'t fetch `{}`'.format(webpage_url))

			if len(info['entries']) < 1:
				raise commands.UserInputError(
					'Couldn\'t find anything that matches `{}`'.format(search))

			info = info['entries'][0]

			output.append(cls(ctx, discord.FFmpegPCMAudio(
				info.get('url'), **cls.FFMPEG_OPTIONS), data=info))

		return output


class Song:
	__slots__ = ('source', 'requester')

	def __init__(self, source: YTDLSource):
		self.source = source
		self.requester = source.requester

	def create_embed(self):
		embed = Embed(title=f"{self.source.title}", url=self.source.url, description=f"""
		**Requester**: {self.requester.mention}
		**Duration**: {self.source.formatted_duration}
		**Artist**: [{self.source.uploader}]({self.source.uploader_url})
		""")
		embed.set_thumbnail(url=self.source.thumbnail)
		return embed


class SongQueue(asyncio.Queue):
	def __getitem__(self, item):
		if isinstance(item, slice):
			return list(itertools.islice(self._queue, item.start, item.stop, item.step))
		else:
			return self._queue[item]

	def __iter__(self):
		return self._queue.__iter__()

	def __len__(self):
		return self.qsize()

	def clear(self):
		self._queue.clear()

	def shuffle(self):
		random.shuffle(self._queue)

	def remove(self, index: int):
		del self._queue[index]


class VoiceState:
	def __init__(self, bot: commands.Bot, guild: discord.Guild):
		self.bot = bot
		self._guild = guild

		self.current = None
		self.voice = None
		self.next = asyncio.Event()
		self.songs = SongQueue()

		self._loop = False
		self._volume = 0.5

		self.audio_player = bot.loop.create_task(self.audio_player_task())

	def __del__(self):
		self.audio_player.cancel()

	@property
	def loop(self):
		return self._loop

	@loop.setter
	def loop(self, value: bool):
		self._loop = value

	@property
	def volume(self):
		return self._volume

	@volume.setter
	def volume(self, value: float):
		self._volume = value

	@property
	def is_playing(self):
		return self.voice and self.current

	async def audio_player_task(self):
		while True:
			self.next.clear()

			if not self.loop:
				try:
					async with timeout(180):  # 3 minutes
						self.current = await self.songs.get()
				except asyncio.TimeoutError:
					self.bot.loop.create_task(self.stop())
					return

			self.current.source.volume = self._volume
			self.voice.play(self.current.source, after=self.play_next_song)
			# TODO when song ends now playing message
			# await self.current.source.channel.send(embed=self.current.create_embed())

			await self.next.wait()

	def play_next_song(self, error=None):
		if error:
			raise commands.UserInputError(str(error))

		self.next.set()

	def skip(self):
		if self.is_playing:
			self.voice.stop()

	async def stop(self):
		self.songs.clear()

		if self.voice:
			await self.voice.disconnect()
			self.voice = None
