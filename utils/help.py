from discord.ext import commands
class ApolloHelp(commands.HelpCommand):
    async def send_bot_help(self, mapping):
        await self.context.send("This is help")

    async def send_command_help(self, command):
        await self.context.send("This is help command")

    async def send_group_help(self, group):
        await self.context.send("This is help group")

    async def send_cog_help(self, cog):
        await self.context.send("This is help cog")

    # @commands.command(name='help', description="Shows all commands", usage="help [command]", aliases=['commands'])
    # async def _help(self, ctx: commands.Context, command: str = None) -> None:
    #     if command:
    #         cmds = [unpack for unpack in self.bot.walk_commands()
    #                 if 'jishaku' not in unpack.module]
    #         cmd = discord.utils.get(cmds, name=command.lower())
    #         if cmd is None:
    #             for c in cmds:
    #                 if command.lower() in c.aliases:
    #                     cmd = c
    #                     break
    #         if cmd is None:
    #             raise commands.BadArgument("Command does not exist.")
    #         if cmd.usage is None:
    #             embed = discord.Embed(
    #                 title=f"`{cmd.name}`", description=cmd.description, color=discord.Color.blurple())
    #         else:
    #             embed = discord.Embed(
    #                 title=f"`{cmd.usage}`", description=cmd.description, color=discord.Color.blurple())
    #         if cmd.aliases != []:
    #             embed.add_field(
    #                 name="Aliases",
    #                 value=', '.join(f'`{aliases}`' for aliases in cmd.aliases),
    #             )
    #         await ctx.reply(embed=embed)
    #     else:
    #         exts = [ext for ext in list(self.bot.extensions.values()) if not ext.__name__ in (
    #             'jishaku', 'cogs.statcord', 'cogs.error')]

    #         class HelpMenu(ViewMenu):
    #             def __init__(self):
    #                 super().__init__(clear_reactions_after=True)
    #                 self.message = None
    #                 self.timeout = 180

    #             async def send_initial_message(self, ctx: commands.Context, channel: discord.Message):
    #                 cogs = ' '.join(
    #                     f"`{ext.__name__.split('.')[1].capitalize()}`" for ext in exts)
    #                 self.message = await self.send_with_view(channel, embed=discord.Embed(title='Apollo Commands', description="stinky :D", color=discord.Color.blurple()))
    #                 return self.message

    #             @menus.button("<:mod:860185459246628864>")
    #             async def moderation(self, interaction):
    #                 if self.ctx.author.id == interaction.user.id:
    #                     cmds = ' '.join(
    #                         f"`{cmd.name}`" for cmd in self.ctx.bot.get_cog('Mod').get_commands())
    #                     await self.message.edit(embed=discord.Embed(title='Moderation Commands', description=f"> {cmds}", color=discord.Color.blurple()))

    #             @menus.button("<:animals:860185151421677598>")
    #             async def animals(self, interaction):
    #                 if self.ctx.author.id == interaction.user.id:
    #                     cmds = ' '.join(
    #                         f"`{cmd.name}`" for cmd in self.ctx.bot.get_cog('Animals').get_commands())
    #                     await self.message.edit(embed=discord.Embed(title='Animals Commands', description=f"> {cmds}", color=discord.Color.blurple()))

    #             @menus.button("<:reddit:860185422474510347>")
    #             async def reddit(self, interaction):
    #                 if self.ctx.author.id == interaction.user.id:
    #                     cmds = ' '.join(
    #                         f"`{cmd.name}`" for cmd in self.ctx.bot.get_cog('Reddit').get_commands())
    #                     await self.message.edit(embed=discord.Embed(title='Reddit Commands', description=f"> {cmds}", color=discord.Color.blurple()))

    #             @menus.button("<:fun:860185588472217631>")
    #             async def fun(self, interaction):
    #                 if self.ctx.author.id == interaction.user.id:
    #                     cmds = ' '.join(
    #                         f"`{cmd.name}`" for cmd in self.ctx.bot.get_cog('Fun').get_commands())
    #                     await self.message.edit(embed=discord.Embed(title='Fun Commands', description=f"> {cmds}", color=discord.Color.blurple()))

    #             @menus.button("<:image:860185695351603230>")
    #             async def image(self, interaction):
    #                 if self.ctx.author.id == interaction.user.id:
    #                     cmds = ' '.join(
    #                         f"`{cmd.name}`" for cmd in self.ctx.bot.get_cog('Image').get_commands())
    #                     await self.message.edit(embed=discord.Embed(title='Image Commands', description=f"> {cmds}", color=discord.Color.blurple()))

    #             @menus.button("<:utility:860185936888332298>")
    #             async def utility(self, interaction):
    #                 if self.ctx.author.id == interaction.user.id:
    #                     cmds = ' '.join(
    #                         f"`{cmd.name}`" for cmd in self.ctx.bot.get_cog('Utility').get_commands())
    #                     await self.message.edit(embed=discord.Embed(title='Utility Commands', description=f"> {cmds}", color=discord.Color.blurple()))

    #             @menus.button("<:games:860186042279395340>")
    #             async def games(self, interaction):
    #                 if self.ctx.author.id == interaction.user.id:
    #                     cmds = ' '.join(
    #                         f"`{cmd.name}`" for cmd in self.ctx.bot.get_cog('Games').get_commands())
    #                     await self.message.edit(embed=discord.Embed(title='Games Commands', description=f"> {cmds}", color=discord.Color.blurple()))

    #             @menus.button("<:meta:860186247255687189>")
    #             async def meta(self, interaction):
    #                 if self.ctx.author.id == interaction.user.id:
    #                     cmds = ' '.join(
    #                         f"`{cmd.name}`" for cmd in self.ctx.bot.get_cog('Meta').get_commands())
    #                     await self.message.edit(embed=discord.Embed(title='Meta Commands', description=f"> {cmds}", color=discord.Color.blurple()))

    #             async def start(self, ctx: commands.Context):
    #                 await super().start(ctx)
    #                 self.ctx = ctx

    #             @menus.button("\N{BLACK SQUARE FOR STOP}\ufe0f")
    #             async def on_stop(self, payload):
    #                 self.stop()

    #         await HelpMenu().start(ctx)