from datetime import datetime
from time import time as count

import discord
import humanize
import pkg_resources
from discord.ext import commands, tasks

from utils.context import ApolloContext
from utils.converters import PrefixConverter


class Meta(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot
        self._status.start()
        self._cd_type = commands.BucketType.user
        self._cd = commands.CooldownMapping.from_cooldown(1, 2., self._cd_type)

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

    def get_uptime(self) -> str:
        return humanize.naturaldelta(datetime.utcnow() - self.bot.uptime)

    @commands.command(name='invite', description="Shows the bot invite.")
    async def _invite(self, ctx: ApolloContext) -> None:
        embed = discord.Embed(title="Apollo Invite", color=discord.Color.blurple())
        embed.add_field(name="Administrator", value=f"[click]({discord.utils.oauth_url(client_id=self.bot.user.id, permissions=discord.Permissions(administrator=True))})", inline=True)
        embed.add_field(name="No Permissions", value=f"[click]({discord.utils.oauth_url(client_id=self.bot.user.id, permissions=discord.Permissions.none())})", inline=True)
        await ctx.reply(embed=embed)

    @commands.command(name='discordbotlist', description="Shows the bot invite.", aliases=['dbl'])
    async def _discordbotlist(self, ctx: ApolloContext) -> None:
        embed = discord.Embed(title="Apollo Bot List", description="Click [here](https://discordbotlist.com/bots/apollo-5670) for the bot list.", color=discord.Color.blurple())
        await ctx.reply(embed=embed)

    @commands.command(name='uptime', description="Shows the bot uptime.")
    async def _uptime(self, ctx: ApolloContext) -> None:
        await ctx.reply(embed=discord.Embed(title="Apollo Uptime", description=f"The bot has been online for `{self.get_uptime()}`.",
                                            color=discord.Color.blurple()))

    @commands.command(name='ping', description="Shows the bot ping.")
    async def _ping(self, ctx: ApolloContext) -> None:
        typing = count()
        m = await ctx.reply("Loading...")
        typing = (count() - typing) * 1000
        database = count()
        await self.bot.db.execute("SELECT 1")
        database = (count() - database) * 1000
        embed = discord.Embed(title="Apollo Ping", color=discord.Color.blurple())
        embed.add_field(name="Websocket",
                        value=f"```py\n{(self.bot.latency * 1000):.2f} ms\n```")
        embed.add_field(name="Typing", value=f"```py\n{typing:.2f} ms\n```")
        embed.add_field(name="Database",
                        value=f"```py\n{database:.2f} ms\n```")
        embed.set_thumbnail(url=self.bot.user.avatar.url)
        await m.edit(content=None, embed=embed)

    @commands.command(name='info', description="Shows information about the bot.")
    async def _info(self, ctx: ApolloContext) -> None:
        embed = discord.Embed(
            title="Apollo Info", description=self.bot.description, color=discord.Color.blurple())
        embed.set_thumbnail(url=self.bot.user.avatar.with_static_format('png'))
        embed.add_field(
            name="Version", value=self.bot.__version__, inline=True)
        owner = self.bot.get_user(331179093447933963)
        embed.add_field(name="Owner", value=owner)
        embed.add_field(
            name="Members", value=f"{sum([guild.member_count for guild in self.bot.guilds]):,}", inline=True)
        embed.add_field(
            name="Guilds", value=f"{len(self.bot.guilds):,}", inline=True)
        embed.add_field(
            name="Uptime", value=f"{self.get_uptime()}", inline=True)
        dpy = pkg_resources.get_distribution('discord.py').version
        embed.add_field(name="discord.py", value=f"v{dpy}")
        await ctx.reply(embed=embed)

    @commands.command(name='source', description="Shows source of the bot.", aliases=['src', 'contribute', 'contrib'])
    async def _source(self, ctx: ApolloContext) -> None:
        await ctx.reply(
            embed=discord.Embed(title="Apollo Source", description="View the bot source [here](https://github.com/SuperOrca/apollo).",
                                color=discord.Color.blurple()))

    @commands.command(name='prefix', description="Change the bot prefix.", usage="prefix [prefix]")
    async def _prefix(self, ctx: ApolloContext, prefix: PrefixConverter = None) -> None:
        if ctx.author.guild_permissions.administrator and prefix:
            await self.bot.db.execute("INSERT OR REPLACE INTO prefixes VALUES (:id, :prefix)",
                                      values={"id": ctx.guild.id, "prefix": prefix})
            await ctx.reply(embed=discord.Embed(title="Apollo Prefix", description=f"Set the server prefix to `{prefix}`.",
                                                color=discord.Color.blurple()))
        else:
            prefix = await self.bot.get_guild_prefix(ctx.message)
            await ctx.reply(embed=discord.Embed(title="Apollo Prefix", description=f"The current server prefix is `{prefix}`.",
                                                color=discord.Color.blurple()))


def setup(bot) -> None:
    bot.add_cog(Meta(bot))
