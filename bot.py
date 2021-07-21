import json
import logging
import sys
import traceback
from collections import Counter
from datetime import datetime
from os import getenv
from pathlib import Path

import aiohttp
import asyncdagpi
import coloredlogs
import discord
import mystbin
import psutil
from aiogtts import aiogTTS
from async_tio import Tio
from databases import Database
from discord.ext import commands
from dotenv import load_dotenv

from utils.context import ApolloContext
from utils.help import ApolloHelp

load_dotenv()


class Apollo(commands.AutoShardedBot):
    @staticmethod
    async def _get_prefix(bot, message: discord.Message):
        return commands.when_mentioned_or(await bot.get_guild_prefix(message))(bot, message)

    def __init__(self) -> None:
        self.connector = aiohttp.TCPConnector(limit=200)
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
        An open-source general-use discord.py bot.
        """
        super().__init__(
            command_prefix=self._get_prefix,
            help_command=ApolloHelp(),
            case_insensitive=True,
            allowed_mentions=allowed_mentions,
            description=description,
            intents=intents,
            activity=discord.Game("@Apollo help"),
            strip_after_prefix=True,
            max_messages=10000,
            connector=self.connector,
        )
        self.__version__ = "1.0.0"
        self.owner_ids = (int(getenv('OWNER_ID')),)
        self.init_logging()
        self.init_constants()

    async def init(self) -> None:
        self.db = Database('sqlite:///bot.db')
        await self.db.connect()
        await self.db.execute(
            "CREATE TABLE IF NOT EXISTS prefixes (id BIGINT PRIMARY KEY, prefix TEXT)"
        )
        await self.db.execute(
            "CREATE TABLE IF NOT EXISTS usage (command TEXT PRIMARY KEY, uses BIGINT)"
        )
        await self.db.execute(
            "CREATE TABLE IF NOT EXISTS economy (id BIGINT PRIMARY KEY, wallet INT, bank INT, bankcap INT, multi INT, daily TIMESTAMP)"
        )
        self.session = aiohttp.ClientSession(
            headers={'User-Agent': "Apollo Bot v{} Python/{}.{} aiohttp/{}".format(
                self.__version__, sys.version_info[0], sys.version_info[1], aiohttp.__version__)},
            timeout=aiohttp.ClientTimeout(total=30),
            loop=self.loop
        )
        self.tio = await Tio(session=self.session, loop=self.loop)
        self.mystbin = mystbin.Client(session=self.session)
        self.dagpi = asyncdagpi.Client(
            getenv('DAGPI'), session=self.session, loop=self.loop)
        self.tts = aiogTTS()
        self.psutil_process = psutil.Process()

    def init_logging(self):
        coloredlogs.install()
        self.log = logging.getLogger('discord')
        self.log.setLevel(logging.INFO)
        handler = logging.FileHandler(
            filename="logs/discord.log", encoding="utf-8", mode="w"
        )
        handler.setFormatter(
            logging.Formatter(
                "%(asctime)s:%(levelname)s:%(name)s: %(message)s")
        )
        self.log.addHandler(handler)

    def init_constants(self):
        self.socket_stats = Counter()

        with open("blacklist.json") as f:
            self.blacklist = json.load(f)
        self.add_check(self.is_blacklisted)
        self.before_invoke(self.before_invoke_)

    async def is_blacklisted(self, ctx: ApolloContext) -> bool:
        return ctx.author.id not in self.blacklist

    async def get_guild_prefix(self, message: discord.Message) -> list:
        try:
            prefix = await self.db.fetch_one(f"SELECT * FROM prefixes WHERE id = :id", values={"id": message.guild.id})
        except AttributeError:
            prefix = None
        return getenv('DEFAULT_PREFIX') if prefix is None else prefix[1]

    async def before_invoke_(self, ctx: ApolloContext) -> None:
        await ctx.trigger_typing()

    async def send_owner(self, content: str = None, **kwargs) -> None:
        await self.get_user(self.owner_ids[0]).send(content, **kwargs)

    def load(self) -> None:
        for file in Path('cogs').glob('**/*.py'):
            *tree, _ = file.parts
            try:
                self.load_extension(f"{'.'.join(tree)}.{file.stem}")
            except Exception as e:
                traceback.print_exception(
                    type(e), e, e.__traceback__, file=sys.stderr)

    async def on_ready(self) -> None:
        self.log.info("Running setup...")
        await self.init()
        if not hasattr(self, 'uptime'):
            self.uptime = datetime.utcnow()
        self.log.info(
            "Bot connected. DWSP latency: " +
            str(round((self.latency * 1000))) + "ms"
        )
        self.load()
        self.load_extension('jishaku')
        self.log.info(f"Extensions loaded ({len(self.extensions)} loaded)")
        self.log.info("Bot ready!")

    async def on_message(self, message: discord.Message) -> None:
        if message.author.bot or isinstance(message.channel, (discord.DMChannel, discord.GroupChannel)):
            return
        if message.content.startswith('jsk') and message.author.id == int(getenv('OWNER_ID')):
            message.content = self.user.mention + " " + message.content
        if self.user.mentioned_in(message):
            return await message.reply(f"The server prefix is `{await self.get_guild_prefix(message)}`.")
        await self.process_commands(message)

    async def on_command_completion(self, ctx: ApolloContext):
        if str(ctx.command.parent) != 'jishaku':
            cmd = str(ctx.command.parent or ctx.command.name)
            data = await self.db.fetch_one("SELECT * FROM usage WHERE command = :command", values={"command": cmd})
            if data is None:
                data = (cmd, 0)
            await self.db.execute("INSERT OR REPLACE INTO usage VALUES (:command, :uses)", values={
                "command": data[0],
                "uses": data[1] + 1
            })

    async def on_guild_remove(self, guild: discord.Guild):
        if not guild:
            return

        self.db.execute("DELETE FROM prefixes WHERE id = :id",
                        values={"id": guild.id})

    @staticmethod
    async def send_error_embed(ctx: ApolloContext, content: str, **kwargs) -> None:
        content = content.replace('"', "`")
        embed = discord.Embed(
            description=f"⚠ {content}", color=discord.Color.red())
        await ctx.reply(embed=embed)

    async def on_command_error(self, ctx: ApolloContext, error) -> None:
        m = None
        if hasattr(ctx.command, 'on_error'):
            return

        _ignored = (commands.CommandNotFound, commands.NoPrivateMessage,
                    commands.DisabledCommand)
        _input = commands.UserInputError

        if isinstance(error, _ignored):
            return
        if isinstance(error, _input):
            m = str(error).replace('"', '`')

        if isinstance(error, commands.MissingRequiredArgument):
            return await self.send_error_embed(ctx,
                                               f"You are missing the required `{error.param.name}` argument in `{ctx.command}`.")
        if isinstance(error, commands.CheckFailure):
            m = f"You are not able to use `{ctx.command}`."
        if isinstance(error, commands.CommandOnCooldown):
            return await self.send_error_embed(ctx,
                                               f"`{ctx.command}` is on cooldown for another `{error.retry_after:.1f} seconds`.")
        if isinstance(error, commands.BotMissingPermissions):
            return await self.send_error_embed(ctx,
                                               f"I am missing the `{', '.join([str(perm).replace('_', ' ') for perm in error.missing_permissions])}` permissions.")
        if isinstance(error, commands.MissingPermissions):
            return await self.send_error_embed(ctx,
                                               f"You are missing the `{', '.join([str(perm).replace('_', ' ') for perm in error.missing_permissions])}` permissions.")

        if m is not None:
            await self.send_error_embed(ctx, m)
        else:
            await self.send_error_embed(
                ctx, "An unknown error has occured. I have contacted the developers."
            )
        await self.send_owner(
            "An exception in a user's command:\n```py\n"
            + "".join(
                traceback.format_exception(
                    type(error), error, error.__traceback__)
            )
            + "\n```"
        )

    async def on_socket_response(self, msg) -> None:
        self.socket_stats[msg.get('t')] += 1

    async def get_context(self, message: discord.Message, *, cls=None):
        return await super().get_context(message, cls=cls or ApolloContext)

    def get_message(self, message_id) -> discord.Message:
        return self._connection._get_message(message_id)

    def run(self) -> None:
        self.log.info("Logging in...")
        super().run(getenv('TOKEN'), reconnect=True)

    async def close(self) -> None:
        with open("blacklist.json", 'w') as f:
            json.dump(self.blacklist, f, indent=4)

        await self.session.close()
        await self.db.disconnect()
        await self.dagpi.close()
        await self.tio.close()
        await self.mystbin.close()
        await super().close()
