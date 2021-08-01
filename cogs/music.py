from typing import Optional
import discord
from discord.ext import commands

import asyncio
import itertools
from async_timeout import timeout
from functools import partial
from youtube_dl import YoutubeDL

from utils.context import ApolloContext

ytdlopts = {
    'format': 'bestaudio/best',
    'outtmpl': 'downloads/%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0'
}

ffmpegopts = {
    'before_options': '-nostdin',
    'options': '-vn'
}

ytdl = YoutubeDL(ytdlopts)


class VoiceConnectionError(commands.CommandError):
    """Custom Exception class for connection errors."""


class InvalidVoiceChannel(VoiceConnectionError):
    """Exception for cases of invalid Voice Channels."""


class YTDLSource(discord.PCMVolumeTransformer):

    def __init__(self, source, *, data, requester):
        super().__init__(source)
        self.requester = requester

        self.title = data.get('title')
        self.web_url = data.get('webpage_url')

    def __getitem__(self, item: str):
        return self.__getattribute__(item)

    @classmethod
    async def create_source(cls, ctx, search: str, *, loop, download=False):
        loop = loop or asyncio.get_event_loop()

        to_run = partial(ytdl.extract_info, url=search, download=download)
        data = await loop.run_in_executor(None, to_run)

        if 'entries' in data:
            data = data['entries'][0]

        await ctx.reply(embed=discord.Embed(description=f'```ini\n[Added {data["title"]} to the Queue.]\n```', color=discord.Color.dark_green()))

        if download:
            source = ytdl.prepare_filename(data)
        else:
            return {'webpage_url': data['webpage_url'], 'requester': ctx.author, 'title': data['title']}

        return cls(discord.FFmpegPCMAudio(source), data=data, requester=ctx.author)

    @classmethod
    async def regather_stream(cls, data, *, loop):
        loop = loop or asyncio.get_event_loop()
        requester = data['requester']

        to_run = partial(ytdl.extract_info,
                         url=data['webpage_url'], download=False)
        data = await loop.run_in_executor(None, to_run)

        return cls(discord.FFmpegPCMAudio(data['url']), data=data, requester=requester)


class MusicPlayer:
    __slots__ = ('bot', '_guild', '_channel', '_cog',
                 'queue', 'next', 'current', 'np', 'volume')

    def __init__(self, ctx):
        self.bot = ctx.bot
        self._guild = ctx.guild
        self._channel = ctx.channel
        self._cog = ctx.cog

        self.queue = asyncio.Queue()
        self.next = asyncio.Event()

        self.np = None  # Now playing message
        self.volume = .5
        self.current = None

        ctx.bot.loop.create_task(self.player_loop())

    async def player_loop(self):
        await self.bot.wait_until_ready()

        while not self.bot.is_closed():
            self.next.clear()

            try:
                # Wait for the next song. If we timeout cancel the player and disconnect...
                async with timeout(300):  # 5 minutes...
                    source = await self.queue.get()
            except asyncio.TimeoutError:
                return self.destroy(self._guild)

            if not isinstance(source, YTDLSource):
                # Source was probably a stream (not downloaded)
                # So we should regather to prevent stream expiration
                try:
                    source = await YTDLSource.regather_stream(source, loop=self.bot.loop)
                except Exception as e:
                    await self._channel.send(f'There was an error processing your song.\n'
                                             f'```css\n[{e}]\n```')
                    continue

            source.volume = self.volume
            self.current = source

            self._guild.voice_client.play(
                source, after=lambda _: self.bot.loop.call_soon_threadsafe(self.next.set))
            self.np = await self._channel.send(f'**Now Playing:** `{source.title}` requested by '
                                               f'`{source.requester}`')
            await self.next.wait()

            # Make sure the FFmpeg process is cleaned up.
            source.cleanup()
            self.current = None

            try:
                # We are no longer playing this song...
                await self.np.delete()
            except discord.HTTPException:
                pass

    def destroy(self, guild):
        return self.bot.loop.create_task(self._cog.cleanup(guild))


class Music:
    __slots__ = ('bot', 'players')

    def __init__(self, bot):
        self.bot = bot
        self.players = {}

    async def cleanup(self, guild: discord.Guild):
        try:
            await guild.voice_client.disconnect()
        except AttributeError:
            pass

        try:
            del self.players[guild.id]
        except KeyError:
            pass

    async def __local_check(self, ctx: ApolloContext):
        if not ctx.guild:
            raise commands.NoPrivateMessage
        return True

    def get_player(self, ctx: ApolloContext):
        try:
            player = self.players[ctx.guild.id]
        except KeyError:
            player = MusicPlayer(ctx)
            self.players[ctx.guild.id] = player

        return player

    @commands.command(name='connect', description="Make the bot connect to your channel.", aliases=['join'])
    async def _connect(self, ctx: ApolloContext, *, channel: Optional[discord.VoiceChannel] = None):
        if not channel:
            try:
                channel = ctx.author.voice.channel
            except AttributeError:
                raise InvalidVoiceChannel(
                    'No channel to join. Please either specify a valid channel or join one.')

        vc = ctx.voice_client

        if vc:
            if vc.channel.id == channel.id:
                return
            try:
                await vc.move_to(channel)
            except asyncio.TimeoutError:
                raise VoiceConnectionError(
                    f'Moving to channel: <{channel}> timed out.')
        else:
            try:
                await channel.connect()
            except asyncio.TimeoutError:
                raise VoiceConnectionError(
                    f'Connecting to channel: <{channel}> timed out.')

        await ctx.reply(embed=discord.Embed(description=f'Connected to: **{channel}**', color=discord.Color.dark_green()))

    @commands.command(name='play', description="Play a song.", aliases=['sing'])
    async def _play(self, ctx: ApolloContext, *, search: commands.clean_content):
        vc = ctx.voice_client

        if not vc:
            await ctx.invoke(self.connect_)

        player = self.get_player(ctx)

        source = await YTDLSource.create_source(ctx, search, loop=self.bot.loop, download=False)

        await player.queue.put(source)

    @commands.command(name='pause', description="Pause the player.")
    async def _pause(self, ctx: ApolloContext):
        vc = ctx.voice_client

        if not vc or not vc.is_playing():
            return await ctx.reply(embed=discord.Embed(description='I am not currently playing anything!', color=discord.Color.dark_green()))
        elif vc.is_paused():
            return

        vc.pause()
        await ctx.reply(embed=discord.Embed(description=f'**`{ctx.author}`**: Paused the song!', color=discord.Color.dark_green()))

    @commands.command(name='resume', description="Resume the player.")
    async def _resume(self, ctx: ApolloContext):
        vc = ctx.voice_client

        if not vc or not vc.is_connected():
            return await ctx.reply(embed=discord.Embed(description='I am not currently playing anything!', color=discord.Color.dark_green()))
        elif not vc.is_paused():
            return

        vc.resume()
        await ctx.reply(embed=discord.Embed(description=f'**`{ctx.author}`**: Resumed the song!', color=discord.Color.dark_green()))

    @commands.command(name='skip', description="Skip the current song.")
    async def _skip(self, ctx: ApolloContext):
        vc = ctx.voice_client

        if not vc or not vc.is_connected():
            return await ctx.reply(embed=discord.Embed(description='I am not currently playing anything!', color=discord.Color.dark_green()))

        if vc.is_paused():
            pass
        elif not vc.is_playing():
            return

        vc.stop()
        await ctx.reply(embed=discord.Embed(description=f'**`{ctx.author}`**: Skipped the song!', color=discord.Color.dark_green()))

    @commands.command(name='queue', description="List the queue.", aliases=['q', 'playlist'])
    async def _queue(self, ctx: ApolloContext):
        vc = ctx.voice_client

        if not vc or not vc.is_connected():
            return await ctx.reply(embed=discord.Embed(description='I am not currently connected to voice!', color=discord.Color.dark_green()))

        player = self.get_player(ctx)
        if player.queue.empty():
            return await ctx.reply(embed=discord.Embed(description='There are currently no more queued songs.', color=discord.Color.dark_green()))

        upcoming = list(itertools.islice(player.queue._queue, 0, 5))

        fmt = '\n'.join(f'**`{_["title"]}`**' for _ in upcoming)
        embed = discord.Embed(
            title=f'Upcoming - Next {len(upcoming)}', description=fmt)

        await ctx.reply(embed=embed)

    @commands.command(name='now_playing', description="Information about the current song.", aliases=['np', 'current', 'currentsong', 'playing'])
    async def _playing(self, ctx: ApolloContext):
        vc = ctx.voice_client

        if not vc or not vc.is_connected():
            return await ctx.reply(embed=discord.Embed(description='I am not currently connected to voice!', color=discord.Color.dark_green()))

        player = self.get_player(ctx)
        if not player.current:
            return await ctx.reply(embed=discord.Embed(description='I am not currently playing anything!', color=discord.Color.dark_green()))

        try:
            await player.np.delete()
        except discord.HTTPException:
            pass

        player.np = await ctx.send(f'**Now Playing:** `{vc.source.title}` '
                                   f'requested by `{vc.source.requester}`')

    @commands.command(name='volume', description="Change the volume of the player.", aliases=['vol'])
    async def _volume(self, ctx: ApolloContext, *, vol: float):
        vc = ctx.voice_client

        if not vc or not vc.is_connected():
            return await ctx.reply(embed=discord.Embed(description='I am not currently connected to voice!', color=discord.Color.dark_green()))

        if not 0 < vol < 101:
            return await ctx.reply(embed=discord.Embed(description='Please enter a value between 1 and 100.', color=discord.Color.dark_green()))

        player = self.get_player(ctx)

        if vc.source:
            vc.source.volume = vol / 100

        player.volume = vol / 100
        await ctx.reply(embed=discord.Embed(description=f'**`{ctx.author}`**: Set the volume to **{vol}%**', color=discord.Color.dark_green()))

    @commands.command(name='stop', description="Stop the player.")
    async def _stop(self, ctx: ApolloContext):
        vc = ctx.voice_client

        if not vc or not vc.is_connected():
            return await ctx.reply(embed=discord.Embed(description='I am not currently playing anything!', color=discord.Color.dark_green()))

        await self.cleanup(ctx.guild)
