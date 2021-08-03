import asyncio
import functools
import itertools
import math
import random
from datetime import timedelta
from typing import Optional

import discord
import youtube_dl
import humanize
from async_timeout import timeout
from discord.ext import commands

from utils.context import ApolloContext
from utils.metrics import Embed
from utils.paginator import EmbedPaginator

# Silence useless bug reports messages
youtube_dl.utils.bug_reports_message = lambda: ''


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
        td = timedelta(seconds=self.raw_duration)
        self.duration = humanize.precisedelta(td)
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
        partial = functools.partial(cls.ytdl.extract_info, search, download=False, process=process)
        return await loop.run_in_executor(None, partial)

    @classmethod
    async def create_source(cls, ctx: ApolloContext, search: str, *, loop: Optional[asyncio.BaseEventLoop] = None):
        loop = loop or asyncio.get_event_loop()

        data = await cls.get_processed_info(cls, search, loop, process=False)

        if data is None:
            raise commands.UserInputError('Couldn\'t find anything that matches `{}`'.format(search))

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
                raise commands.UserInputError('Couldn\'t fetch `{}`'.format(webpage_url))

            for entry in info['entries']:
                output.append(cls(ctx, discord.FFmpegPCMAudio(entry.get('url'), **cls.FFMPEG_OPTIONS), data=entry))
        else:
            webpage_url = data.get('webpage_url', data.get('url'))
            info = await cls.get_processed_info(cls, webpage_url, loop)

            if info is None:
                raise commands.UserInputError('Couldn\'t fetch `{}`'.format(webpage_url))

            if len(info['entries']) < 1:
                raise commands.UserInputError(
                        'Couldn\'t find anything that matches `{}`'.format(search))
            
            info = info['entries'][0]

            output.append(cls(ctx, discord.FFmpegPCMAudio(info.get('url'), **cls.FFMPEG_OPTIONS), data=info))

        return output


class Song:
    __slots__ = ('source', 'requester')

    def __init__(self, source: YTDLSource):
        self.source = source
        self.requester = source.requester

    def create_embed(self):
        embed = Embed(title=f"{self.source.title}", url=self.source.url, description=f"""
		**Requester**: {self.requester.mention}
		**Duration**: {self.source.duration}
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

    # @commands.command(name='volume', description="Sets the volume of the player.")
    # async def _volume(self, ctx: ApolloContext, volume: int):
    #     await self.ensure_voice_state(ctx)

    #     if not ctx.voice_state.is_playing:
    #         raise commands.UserInputError('Nothing being played at the moment.')

    #     if 0 > volume > 100:
    #         raise commands.UserInputError('Volume must be between 0 and 100')

    #     ctx.voice_state.volume = volume / 100
    #     await ctx.tick()

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

            queue = ''
            for i, song in enumerate(ctx.voice_state.songs[start:end], start=start):
                queue += '{0}. [{1.source.title}]({1.source.url}) | {1.source.requester.mention}\n'.format(
                    i + 1, song)

            embeds.append(Embed(title=f'{len(ctx.voice_state.songs)} tracks', description=queue)
                    .set_footer(text='Viewing page {}/{}'.format(page, pages)))
        EmbedPaginator.start(ctx, embeds)

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
