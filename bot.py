import logging
import sys
import traceback
from datetime import datetime
from os import getenv, environ
from pathlib import Path
import re

import aiosqlite
import coloredlogs
import discord
import mystbin
import aiohttp
from utils.help import ApolloHelp
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()


class Context(commands.Context):
    @discord.utils.copy_doc(discord.Message.reply)
    async def reply(self, content:str=None, **kwargs):
        return await self.message.reply(content, **kwargs, mention_author=False)


class Apollo(commands.Bot):
    @staticmethod
    async def _get_prefix(bot, message):
        async with bot.db as db:
            cursor = await db.execute("SELECT * FROM prefixes WHERE id=?", (message.guild.id,))
            row = await cursor.fetchone()
            await cursor.close()
            return commands.when_mentioned_or(row[1])(bot, message) if row is not None else commands.when_mentioned_or(
                getenv('DEFAULT_PREFIX'))(bot, message)

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

    async def create_db(self) -> None:
        async with self.db as db:
            await db.execute("CREATE TABLE IF NOT EXISTS prefixes (id INTEGER PRIMARY KEY, prefix TEXT)")

    @property
    def db(self):
        return aiosqlite.connect('bot.db')

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
        await self.create_db()
        if not hasattr(self, 'uptime'):
            self.uptime = datetime.utcnow()
        self.log.info("Bot connected. DWSP latency: " +
                      str(round((self.latency * 1000))) + "ms")
        self.load()
        self.load_extension('jishaku')
        environ['JISHAKU_UNDERSCORE'] = 'True'
        environ['JISHAKU_HIDE'] = 'True'
        self.log.info(f"Extensions loaded ({len(self.extensions)} loaded)")
        self.log.info("Bot ready!")

    async def on_message(self, message: discord.Message) -> None:
        if message.author.bot or isinstance(message.channel, (discord.DMChannel, discord.GroupChannel)):
            return
        if message.content.startswith('jsk') and message.author.id == int(getenv('OWNER_ID')):
            message.content = self.user.mention + " " + message.content
        await self.process_commands(message)

    async def get_context(self, message: discord.Message, *, cls=None):
        return await super().get_context(message, cls=cls or Context)

    def run(self) -> None:
        self.log.info("Logging in...")
        super().run(getenv('TOKEN'), reconnect=True)

    async def close(self) -> None:
        await self.session.close()
        await super().close()
