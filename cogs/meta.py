from os import getenv

import discord
import pkg_resources
from discord.ext import commands, tasks
from time import time as count
from discord.ext import menus
from discord.ext.menus.views import ViewMenu

from utils import time
from utils.converters import PrefixConverter


class Meta(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot
        self.status = ['Watching time pass', 'Rick Astley']
        self.status_next = 0
        self._status.start()

    @tasks.loop(minutes=2.)
    async def _status(self) -> None:
        prefix = getenv('DEFAULT_PREFIX')
        await self.bot.change_presence(activity=discord.Game(f"{prefix}help | " + self.status[self.status_next]))
        self.status_next += 1
        if self.status_next > (len(self.status) - 1):
            self.status_next = 0

    def cog_unload(self) -> None:
        self._status.cancel()

    def get_uptime(self, brief=False) -> str:
        return time.human_timedelta(self.bot.uptime, brief=brief)

    @commands.command(name='stats', description="Shows the bot stats.")
    async def _stats(self, ctx) -> None:
        await ctx.reply(
            embed=discord.Embed(description="View the bot stats [here](https://statcord.com/bot/847566539607769089).",
                                color=discord.Color.blurple()))

    @commands.command(name='invite', description="Shows the bot invite.")
    async def _invite(self, ctx) -> None:
        await ctx.reply(embed=discord.Embed(
            description="Invite the bot [here](https://discord.com/api/oauth2/authorize?client_id=847566539607769089&permissions=8&scope=bot).",
            color=discord.Color.blurple()))

    @commands.command(name='uptime', description="Shows the bot uptime.")
    async def _uptime(self, ctx) -> None:
        await ctx.reply(embed=discord.Embed(description=f"The bot has been online for `{self.get_uptime()}`.",
                                            color=discord.Color.blurple()))

    @commands.command(name='ping', description="Shows the bot ping.")
    async def _ping(self, ctx) -> None:
        typing = count()
        async with ctx.typing():
            typing = (count() - typing) * 1000
            database = count()
            async with self.bot.db as db:
                await db.execute("SELECT 1")
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
    async def _info(self, ctx) -> None:
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
            name="Uptime", value=f"{self.get_uptime(brief=True)}", inline=True)
        dpy = pkg_resources.get_distribution('discord.py').version
        embed.add_field(name="discord.py", value=f"v{dpy}")
        await ctx.reply(embed=embed)

    @commands.command(name='source', description="Shows source of the bot.", aliases=['src', 'contribute', 'contrib'])
    async def _source(self, ctx) -> None:
        await ctx.reply(
            embed=discord.Embed(description="View the bot source [here](https://github.com/SuperOrca/apollo).",
                                color=discord.Color.blurple()))

    @commands.command(name='help', description="Shows all commands", usage="help [command]", aliases=['commands'])
    async def _help(self, ctx, command: str = None) -> None:
        if command:
            cmds = [unpack for unpack in self.bot.walk_commands()
                    if 'jishaku' not in unpack.module]
            cmd = discord.utils.get(cmds, name=command.lower())
            if cmd is None:
                for c in cmds:
                    if command.lower() in c.aliases:
                        cmd = c
                        break
            if cmd is None:
                raise commands.BadArgument("Command does not exist.")
            if cmd.usage is None:
                embed = discord.Embed(
                    title=f"`{cmd.name}`", description=cmd.description, color=discord.Color.blurple())
            else:
                embed = discord.Embed(
                    title=f"`{cmd.usage}`", description=cmd.description, color=discord.Color.blurple())
            if cmd.aliases != []:
                embed.add_field(
                    name="Aliases",
                    value=', '.join(f'`{aliases}`' for aliases in cmd.aliases),
                )
            await ctx.reply(embed=embed)
        else:
            exts = [ext for ext in list(self.bot.extensions.values()) if not ext.__name__ in (
                'jishaku', 'cogs.statcord', 'cogs.error')]

            class HelpMenu(ViewMenu):
                def __init__(self):
                    super().__init__(clear_reactions_after=True)
                    self.message = None
                    self.timeout = 180

                async def send_initial_message(self, ctx, channel):
                    cogs = ' '.join(
                        f"`{ext.__name__.split('.')[1].capitalize()}`" for ext in exts)
                    self.message = await self.send_with_view(channel, embed=discord.Embed(title='Apollo Commands', description="stinky :D", color=discord.Color.blurple()))
                    return self.message

                @menus.button("<:mod:860185459246628864>")
                async def moderation(self, interaction):
                    if self.ctx.author.id == interaction.user.id:
                        cmds = ' '.join(
                            f"`{cmd.name}`" for cmd in self.ctx.bot.get_cog('Mod').get_commands())
                        await self.message.edit(embed=discord.Embed(title='Moderation Commands', description=f"> {cmds}", color=discord.Color.blurple()))

                @menus.button("<:animals:860185151421677598>")
                async def animals(self, interaction):
                    if self.ctx.author.id == interaction.user.id:
                        cmds = ' '.join(
                            f"`{cmd.name}`" for cmd in self.ctx.bot.get_cog('Animals').get_commands())
                        await self.message.edit(embed=discord.Embed(title='Animals Commands', description=f"> {cmds}", color=discord.Color.blurple()))

                @menus.button("<:reddit:860185422474510347>")
                async def reddit(self, interaction):
                    if self.ctx.author.id == interaction.user.id:
                        cmds = ' '.join(
                            f"`{cmd.name}`" for cmd in self.ctx.bot.get_cog('Reddit').get_commands())
                        await self.message.edit(embed=discord.Embed(title='Reddit Commands', description=f"> {cmds}", color=discord.Color.blurple()))

                @menus.button("<:fun:860185588472217631>")
                async def fun(self, interaction):
                    if self.ctx.author.id == interaction.user.id:
                        cmds = ' '.join(
                            f"`{cmd.name}`" for cmd in self.ctx.bot.get_cog('Fun').get_commands())
                        await self.message.edit(embed=discord.Embed(title='Fun Commands', description=f"> {cmds}", color=discord.Color.blurple()))

                @menus.button("<:image:860185695351603230>")
                async def image(self, interaction):
                    if self.ctx.author.id == interaction.user.id:
                        cmds = ' '.join(
                            f"`{cmd.name}`" for cmd in self.ctx.bot.get_cog('Image').get_commands())
                        await self.message.edit(embed=discord.Embed(title='Image Commands', description=f"> {cmds}", color=discord.Color.blurple()))

                @menus.button("<:utility:860185936888332298>")
                async def utility(self, interaction):
                    if self.ctx.author.id == interaction.user.id:
                        cmds = ' '.join(
                            f"`{cmd.name}`" for cmd in self.ctx.bot.get_cog('Utility').get_commands())
                        await self.message.edit(embed=discord.Embed(title='Utility Commands', description=f"> {cmds}", color=discord.Color.blurple()))

                @menus.button("<:games:860186042279395340>")
                async def games(self, interaction):
                    if self.ctx.author.id == interaction.user.id:
                        cmds = ' '.join(
                            f"`{cmd.name}`" for cmd in self.ctx.bot.get_cog('Games').get_commands())
                        await self.message.edit(embed=discord.Embed(title='Games Commands', description=f"> {cmds}", color=discord.Color.blurple()))

                @menus.button("<:meta:860186247255687189>")
                async def meta(self, interaction):
                    if self.ctx.author.id == interaction.user.id:
                        cmds = ' '.join(
                            f"`{cmd.name}`" for cmd in self.ctx.bot.get_cog('Meta').get_commands())
                        await self.message.edit(embed=discord.Embed(title='Meta Commands', description=f"> {cmds}", color=discord.Color.blurple()))

                async def start(self, ctx):
                    await super().start(ctx)
                    self.ctx = ctx

                @menus.button("\N{BLACK SQUARE FOR STOP}\ufe0f")
                async def on_stop(self, payload):
                    self.stop()

            await HelpMenu().start(ctx)

    @commands.command(name='prefix', description="Change the bot prefix.", usage="prefix [prefix]")
    async def _prefix(self, ctx, prefix: PrefixConverter = None) -> None:
        if ctx.author.guild_permissions.administrator and prefix:
            async with self.bot.db as db:
                await db.execute("INSERT OR REPLACE INTO prefixes VALUES (?, ?)", (ctx.guild.id, prefix))
                await db.commit()
            await ctx.reply(embed=discord.Embed(description=f"Set the server prefix to `{prefix}`.",
                                                color=discord.Color.blurple()))
        else:
            async with self.bot.db as db:
                cursor = await db.execute("SELECT * FROM prefixes WHERE id=?", (ctx.guild.id,))
                row = await cursor.fetchone()
                await cursor.close()
            if row is not None:
                await ctx.reply(embed=discord.Embed(description=f"The current server prefix is `{row[1]}`.",
                                                    color=discord.Color.blurple()))
            else:
                await ctx.reply(mention_author=False,
                                embed=discord.Embed(
                                    description=f"The current server prefix is `{getenv('DEFAULT_PREFIX')}`.",
                                    color=discord.Color.blurple()))


def setup(bot) -> None:
    bot.add_cog(Meta(bot))
