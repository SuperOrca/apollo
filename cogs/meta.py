from datetime import datetime
from time import time as count
from typing import Optional

import discord
import humanize
import pkg_resources
from discord.ext import commands, tasks

from utils.context import ApolloContext
from utils.converters import PrefixConverter
from utils.metrics import Embed
from utils.help import ApolloHelp


class Meta(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot
        self._status.start()
        self._cd_type = commands.BucketType.user
        self._cd = commands.CooldownMapping.from_cooldown(1, 2., self._cd_type)
        self._original_help_command = bot.help_command
        bot.help_command = ApolloHelp()
        bot.help_command.cog = self

    def cog_unload(self):
        self.bot.help_command = self._original_help_command

    async def cog_check(self, ctx: ApolloContext):
        bucket = self._cd.get_bucket(ctx.message)
        retry_after = bucket.update_rate_limit()
        if retry_after:
            raise commands.CommandOnCooldown(
                self._cd, retry_after, self._cd_type)
        else:
            return True

    @tasks.loop(minutes=2.)
    async def _status(self) -> None:
        await self.bot.change_presence(activity=discord.Game(f"@Apollo help | {len(self.bot.guilds)} guilds"))

    def cog_unload(self) -> None:
        self._status.cancel()

    def get_uptime(self, breif=False) -> str:
        if breif:
            return humanize.naturaldelta(discord.utils.utcnow() - self.bot.uptime)
        else:
            return humanize.precisedelta(discord.utils.utcnow() - self.bot.uptime)

    @commands.command(name='invite', description="Shows the bot invite.")
    async def _invite(self, ctx: ApolloContext) -> None:
        embed = Embed(title="Apollo Invite", description=f"""
		**Administrator**: [click]({discord.utils.oauth_url(client_id=self.bot.user.id, permissions=discord.Permissions(administrator=True))})
		**No Permissions**: [click]({discord.utils.oauth_url(client_id=self.bot.user.id, permissions=discord.Permissions.none())})
		""")
        await ctx.reply(embed=embed)

    @commands.command(name='discordbotlist', description="Shows the discordbotlist profile.", aliases=['dbl'])
    async def _discordbotlist(self, ctx: ApolloContext) -> None:
        embed = Embed(title="Apollo Bot List",
                      description="Click [here](https://discordbotlist.com/bots/apollo-5670) for the bot list.")
        await ctx.reply(embed=embed)

    @commands.command(name='discordbotsgg', description="Shows the discordbotsgg profile.", aliases=['dbgg'])
    async def _discordbotsgg(self, ctx: ApolloContext) -> None:
        embed = Embed(title="Apollo Bot List",
                      description="Click [here](https://discord.bots.gg/bots/847566539607769089) for the bot list.")
        await ctx.reply(embed=embed)

    @commands.command(name='uptime', description="Shows the bot uptime.")
    async def _uptime(self, ctx: ApolloContext) -> None:
        await ctx.reply(
            embed=Embed(title="Apollo Uptime", description=f"The bot has been online for `{self.get_uptime()}`."))

    @commands.command(name='ping', description="Shows the bot ping.")
    async def _ping(self, ctx: ApolloContext) -> None:
        typing = count()
        m = await ctx.reply("Loading...")
        typing = (count() - typing) * 1000
        database = count()
        await self.bot.db.execute("SELECT 1")
        database = (count() - database) * 1000
        embed = Embed(title="Apollo Ping", description=f"""
		**Websocket**: {(self.bot.latency * 1000):.2f}ms
		**Typing**: {typing:.2f}ms
		**Database:** {database:.2f}ms
		""")
        embed.set_thumbnail(url=self.bot.user.avatar.url)
        await m.edit(content=None, embed=embed)

    @commands.command(name='info', description="Shows information about the bot.")
    async def _info(self, ctx: ApolloContext) -> None:
        owner = self.bot.get_user(self.bot.owner_ids[0])
        dpy = pkg_resources.get_distribution('discord.py').version
        embed = Embed(
            title="Apollo Info", description=f"""
            **Description:** {self.bot.description}
			**Version**: {self.bot.__version__}
			**Owner**: {owner}
			**Members**: {sum([guild.member_count for guild in self.bot.guilds]):,}
			**Guilds**: {len(self.bot.guilds):,}
			**Uptime**: {self.get_uptime(breif=True)}
			**discord.py**: v{dpy}
			""")
        await ctx.reply(embed=embed)

    @commands.command(name='source', description="Shows source of the bot.", aliases=['src', 'contribute', 'contrib'])
    async def _source(self, ctx: ApolloContext) -> None:
        await ctx.reply(
            embed=Embed(title="Apollo Source",
                        description="View the bot source [here](https://github.com/SuperOrca/apollo)."))

    @commands.command(name='prefix', description="Change the bot prefix.", usage="[prefix]")
    async def _prefix(self, ctx: ApolloContext, prefix: Optional[PrefixConverter] = None) -> None:
        if ctx.author.guild_permissions.administrator and prefix:
            await self.bot.db.execute("INSERT OR REPLACE INTO prefixes VALUES (:id, :prefix)",
                                      values={"id": ctx.guild.id, "prefix": prefix})
            self.bot.cache["prefixes"][ctx.guild.id] = prefix
            await ctx.reply(embed=Embed(title="Apollo Prefix", description=f"Set the server prefix to `{prefix}`."))
        else:
            prefix = await self.bot.get_guild_prefix(ctx.message)
            await ctx.reply(embed=Embed(title="Apollo Prefix", description=f"The current server prefix is `{prefix}`."))


def setup(bot) -> None:
    bot.add_cog(Meta(bot))
