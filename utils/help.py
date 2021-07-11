import discord
from discord.ext import commands


class ApolloHelp(commands.HelpCommand):
    async def send_bot_help(self, mapping: dict):
        prefix = await self.context.bot.get_guild_prefix(self.context.message)
        modules = list(mapping.keys())[:-2]
        valid_commands = []
        for module in modules:
            valid_commands += module.get_commands()
        embed = discord.Embed(title="Apollo Help", description=f"""
Total Commands: `{len(valid_commands)}`
```diff
- ⚠️ DO NOT TYPE THESE WHEN USING A COMMAND ⚠️
- <> | Required Argument
- [] | Optional Argument
+ Type {prefix}help [Command | Module] for more info on a command and/or module!
```
`{prefix}invite` | `{prefix}info`
""", color=discord.Color.blurple())
        embed.add_field(
            name=f":gear: Modules [{len(modules)}]",
            value='\n'.join(
                f"- `{module.__class__.__name__}`" for module in modules),
            inline=True,
        )
        embed.add_field(name=":newspaper: News - July 9, 2021",
                        value="Invite my bot to ur server pls :)")
        await self.context.reply(embed=embed)

    async def send_command_help(self, command: commands.Command):
        embed = discord.Embed(
            title=f"**`{command.usage if command.usage is not None else command.name}`**", description=command.description, color=discord.Color.blurple())
        embed.add_field(
            name="Module", value=command.cog_name)
        if command.aliases != []:
            embed.add_field(name=f"Aliases [{len(command.aliases)}]", value=', '.join(
                f'`{aliase}`' for aliase in command.aliases))
        embed.add_field(name="Enabled?", value=command.enabled)
        embed.add_field(name="Hidden?", value=command.hidden)
        if command._buckets._cooldown is not None:
            embed.add_field(
                name="Cooldown", value=f"{command._buckets._cooldown.per} seconds")
        await self.context.reply(embed=embed)

    async def send_group_help(self, group: commands.Group):
        print(group, dir(group))

    async def send_cog_help(self, cog: commands.Cog):
        prefix = await self.context.bot.get_guild_prefix(self.context.message)
        embed = discord.Embed(title=f"{cog.__class__.__name__} Help [{len(cog.get_commands())}]", description=f"""
```diff
- ⚠️ DO NOT TYPE THESE WHEN USING A COMMAND ⚠️
- <> | Required Argument
- [] | Optional Argument
+ Type {prefix}help [Command | Module] for more info on a command and/or module!
```
> {', '.join(f'`{cmd.name}`' for cmd in cog.get_commands())}
        """, color=discord.Color.blurple())
        await self.context.reply(embed=embed)
