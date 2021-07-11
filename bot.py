import logging
import sys
import traceback
from datetime import datetime
from os import getenv, environ
from pathlib import Path
import re

import coloredlogs
import discord
import mystbin
import asyncdagpi
import aiohttp
import statcord
from aiogtts import aiogTTS
from async_tio import Tio
from databases import Database
from utils.help import ApolloHelp
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()


class Context(commands.Context):
    @discord.utils.copy_doc(discord.Message.reply)
    async def reply(self, content: str = None, **kwargs):
        return await self.message.reply(content, **kwargs, mention_author=False)


class Apollo(commands.Bot):
    @staticmethod
    async def _get_prefix(bot, message: discord.Message):
        return commands.when_mentioned_or(await bot.get_guild_prefix(message))(bot, message)

    def __init__(self) -> None:
        allowed_mentions = discord.AllowedMentions.none()
        intents = discord.Intents(
            guilds=True,
            members=True,
            bans=True,
            emojis=True,
            voice_states=True,
            messages=True,
            reactions=True
        )
        description = """
        The all-in-one discord bot.
        """
        super().__init__(command_prefix=self._get_prefix, help_command=ApolloHelp(), case_insensitive=True,
                         allowed_mentions=allowed_mentions, description=description, intents=intents,
                         activity=discord.Game(f'@Apollo help'))
        self.__version__ = "v1.0.0"
        self.owner_id = int(getenv('OWNER_ID'))
        coloredlogs.install()
        self.log = logging.getLogger('discord')
        self.log.setLevel(logging.INFO)
        handler = logging.FileHandler(
            filename="logs/discord.log", encoding='utf-8', mode='w')
        handler.setFormatter(logging.Formatter(
            '%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
        self.log.addHandler(handler)
        self.session = aiohttp.ClientSession()
        self.mystbin = mystbin.Client()
        self.statcord = statcord.Client(self, environ["STATCORD"])
        self.statcord.start_loop()
        self.db = None
        self.dagpi = asyncdagpi.Client(getenv('DAGPI'))
        self.tts = aiogTTS()
        self.tio = None

    async def create(self) -> None:
        self.db = Database('sqlite:///bot.db')
        await self.db.connect()
        await self.db.execute("CREATE TABLE IF NOT EXISTS prefixes (id INTEGER PRIMARY KEY, prefix TEXT)")
        self.tio = await Tio()

    async def get_guild_prefix(self, message: discord.Message):
        try:
            prefix = await self.db.fetch_one(f"SELECT * FROM prefixes WHERE id=:id", values={"id": message.guild.id})
        except AttributeError:
            prefix = None
        return getenv('DEFAULT_PREFIX') if prefix is None else prefix[1]

    def load(self):
        for file in Path('cogs').glob('**/*.py'):
            *tree, _ = file.parts
            try:
                self.load_extension(f"{'.'.join(tree)}.{file.stem}")
            except Exception as e:
                traceback.print_exception(
                    type(e), e, e.__traceback__, file=sys.stderr)

    async def on_ready(self) -> None:
        self.log.info("Running setup...")
        await self.create()
        if not hasattr(self, 'uptime'):
            self.uptime = datetime.utcnow()
        self.log.info("Bot connected. DWSP latency: " +
                      str(round((self.latency * 1000))) + "ms")
        self.load()
        self.load_extension('jishaku')
        self.log.info(f"Extensions loaded ({len(self.extensions)} loaded)")
        self.log.info("Bot ready!")

    async def on_message(self, message: discord.Message) -> None:
        if message.author.bot or isinstance(message.channel, (discord.DMChannel, discord.GroupChannel)):
            return
        if message.content.startswith('jsk') and message.author.id == int(getenv('OWNER_ID')):
            message.content = self.user.mention + " " + message.content
        await self.process_commands(message)

    async def on_command_error(self, ctx: commands.Context, error) -> None:
        if hasattr(ctx.command, 'on_error'):
            return

        ignored = (commands.CommandNotFound,
                   commands.DisabledCommand, commands.NoPrivateMessage)

        if isinstance(error, ignored):
            return

        if isinstance(error, commands.MissingRequiredArgument):
            error = f"You are missing the required `{str(error).split()[0].upper()}` argument."

        self.log.error(f"{ctx.command} -> {error}")
        await ctx.send(embed=discord.Embed(description=error, color=discord.Color.red()))

    async def on_command(self, ctx: commands.Context) -> None:
        self.statcord.command_run(ctx)

    async def get_context(self, message: discord.Message, *, cls=None):
        return await super().get_context(message, cls=cls or Context)

    def run(self) -> None:
        self.log.info("Logging in...")
        super().run(getenv('TOKEN'), reconnect=True)

    async def close(self) -> None:
        await self.session.close()
        await self.db.disconnect()
        await self.dagpi.close()
        await self.tio.close()
        await self.mystbin.close()
        await super().close()
