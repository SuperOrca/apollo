from os import getenv

import discord
import pkg_resources
import humanize
from discord.ext import commands, tasks
from datetime import datetime
from time import time as count
from discord.ext import menus
from discord.ext.menus.views import ViewMenu

from utils.converters import PrefixConverter


class Meta(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot
        self._status.start()

    @tasks.loop(minutes=2.)
    async def _status(self) -> None:
        await self.bot.change_presence(activity=discord.Game(f"@Apollo help | {len(self.bot.guilds)} guilds"))

    def cog_unload(self) -> None:
        self._status.cancel()

    def get_uptime(self) -> str:
        return humanize.naturaldelta(datetime.utcnow() - self.bot.uptime)

    @commands.command(name='stats', description="Shows the bot stats.")
    async def _stats(self, ctx: commands.Context) -> None:
        await ctx.reply(
            embed=discord.Embed(description="View the bot stats [here](https://statcord.com/bot/847566539607769089).",
                                color=discord.Color.blurple()))

    @commands.command(name='invite', description="Shows the bot invite.")
    async def _invite(self, ctx: commands.Context) -> None:
        await ctx.reply(embed=discord.Embed(
            description="Invite the bot [here](https://discord.com/api/oauth2/authorize?client_id=847566539607769089&permissions=8&scope=bot).",
            color=discord.Color.blurple()))

    @commands.command(name='uptime', description="Shows the bot uptime.")
    async def _uptime(self, ctx: commands.Context) -> None:
        await ctx.reply(embed=discord.Embed(description=f"The bot has been online for `{self.get_uptime()}`.",
                                            color=discord.Color.blurple()))

    @commands.command(name='ping', description="Shows the bot ping.")
    async def _ping(self, ctx: commands.Context) -> None:
        typing = count()
        async with ctx.typing():
            typing = (count() - typing) * 1000
            database = count()
            await self.bot.db.execute("SELECT 1")
            database = (count() - database) * 1000
        embed = discord.Embed(color=discord.Color.blurple())
        embed.add_field(name="Websocket",
                        value=f"```py\n{(self.bot.latency * 1000):.2f} ms\n```")
        embed.add_field(name="Typing", value=f"```py\n{typing:.2f} ms\n```")
        embed.add_field(name="Database",
                        value=f"```py\n{database:.2f} ms\n```")
        embed.set_thumbnail(url=self.bot.user.avatar.url)
        await ctx.reply(embed=embed)

    @commands.command(name='info', description="Shows information about the bot.")
    async def _info(self, ctx: commands.Context) -> None:
        embed = discord.Embed(
            title=self.bot.user.name, description=self.bot.description, color=discord.Color.blurple())
        embed.set_thumbnail(url=self.bot.user.avatar.with_static_format('png'))
        embed.add_field(
            name="Version", value=self.bot.__version__, inline=True)
        owner = self.bot.get_user(331179093447933963)
        embed.add_field(name="Owner", value=owner)
        embed.add_field(
            name="Members", value=f"{len(self.bot.users):,}", inline=True)
        embed.add_field(
            name="Guilds", value=f"{len(self.bot.guilds):,}", inline=True)
        embed.add_field(
            name="Uptime", value=f"{self.get_uptime()}", inline=True)
        dpy = pkg_resources.get_distribution('discord.py').version
        embed.add_field(name="discord.py", value=f"v{dpy}")
        await ctx.reply(embed=embed)

    @commands.command(name='source', description="Shows source of the bot.", aliases=['src', 'contribute', 'contrib'])
    async def _source(self, ctx: commands.Context) -> None:
        await ctx.reply(
            embed=discord.Embed(description="View the bot source [here](https://github.com/SuperOrca/apollo).",
                                color=discord.Color.blurple()))

    @commands.command(name='prefix', description="Change the bot prefix.", usage="prefix [prefix]")
    async def _prefix(self, ctx: commands.Context, prefix: PrefixConverter = None) -> None:
        if ctx.author.guild_permissions.administrator and prefix:
            await self.bot.db.execute("INSERT OR REPLACE INTO prefixes VALUES (?, ?)", (ctx.guild.id, prefix))
            await ctx.reply(embed=discord.Embed(description=f"Set the server prefix to `{prefix}`.",
                                                color=discord.Color.blurple()))
        else:
            prefix = await self.bot.get_guild_prefix(ctx.message)
            await ctx.reply(embed=discord.Embed(description=f"The current server prefix is `{prefix[1]}`.",
                                                color=discord.Color.blurple()))


def setup(bot) -> None:
    bot.add_cog(Meta(bot))
