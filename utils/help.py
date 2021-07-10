import discord
from discord.ext import commands


class ApolloHelp(commands.HelpCommand):
    async def send_bot_help(self, mapping: dict):
        modules = list(mapping.keys())[:-2]
        valid_commands = []
        # for module in modules:
        #     valid_commands += module.
        embed = discord.Embed(title="Apollo Help", description=f"""
Total Commands: `{len(valid_commands)}`
```diff
- <> | Required Argument
- [] | Optional Argument
+ Type >help [Command | Module] for more info on a command and/or module!
```
`?invite` | `?info`
""", color=discord.Color.blurple())
        embed.add_field(
            name=":gear: Modules",
            value='\n'.join(f"- `{module.__class__.__name__}`" for module in modules),
            inline=True,
        )
        embed.add_field(name=":newspaper: News", value="Invite my bot to ur server pls :)")
        await self.context.send(embed=embed)

    async def send_command_help(self, command):
        print(command)

    async def send_group_help(self, group):
        print(group)

    async def send_cog_help(self, cog):
        print(cog)
