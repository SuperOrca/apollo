import discord
from discord.ext import commands
import io
from aiogtts import aiogTTS
from async_tio import Tio
import humanize

class Utility(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot
        self.tts = aiogTTS()
        self.tio = Tio()

    @commands.command(name='avatar', description="Shows a user's avatar.", usage="avatar [member]")
    async def _avatar(self, ctx, member: commands.MemberConverter = None) -> None:
        member = member or ctx.author
        embed = discord.Embed(
            description=f"[png]({member.avatar_url_as(static_format='png')}) | [jpg]({member.avatar_url_as(static_format='jpg')}) | [webp]({member.avatar_url_as(static_format='webp')})",
            color=0x2F3136)
        embed.set_image(url=member.avatar_url_as(static_format='png'))
        await ctx.reply(embed=embed)

    @commands.command(name='pypi', description="Shows details of a python package.", usage="pypi <package>")
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def _pypi(self, ctx, package: str) -> None:
        async with ctx.typing():
            data = await self.bot.session.get(f"https://pypi.org/pypi/{package}/json")

        if data.status != 200:
            raise commands.BadArgument("Invalid package.")

        data = (await data.json())['info']
        embed = discord.Embed(
            title=data['name'], description=data.get('summary', ''), url=data.get('project_url', 'https://pypi.org/'),
            color=0x2F3136)
        if data['version'] != "":
            embed.add_field(
                name="Version", value=data.get('version', 'N/A'))
        if data['license'] != "":
            embed.add_field(
                name="License", value=data.get('license', 'N/A'))
        if data['author'] != "":
            embed.add_field(name="Author", value=data.get('author', 'N/A'))
        if data.get('project_urls', None) is not None:
            for title, url in data.get('project_urls', {}).items():
                embed.add_field(
                    name=title, value=f"[click]({url})", inline=True)
        f = discord.File('assets/python_logo.png', 'pypi.png')
        embed.set_thumbnail(url="attachment://pypi.png")
        await ctx.reply(embed=embed, file=f)

    @commands.command(name='npm', description="Shows details of a node package.", usage="npm <package>")
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def _npm(self, ctx, package: str):
        async with ctx.typing():
            data = await (await self.bot.session.get(f"https://api.npms.io/v2/package/{package}")).json()
        if 'CODE' in data or 'collected' not in data:
            raise commands.BadArgument("Invalid package.")

        data = data['collected']['metadata']
        embed = discord.Embed(title=data['name'], description=data.get(
            'description', ''), url=data['links']['npm'], color=0x2F3136)
        embed.add_field(name="Version", value=data['version'])
        if 'license' in data:
            embed.add_field(name="License", value=data['license'])
        embed.add_field(name="Author", value=data['publisher']['username'])
        for title, url in data['links'].items():
            if title != "npm":
                embed.add_field(name=title.capitalize(),
                                value=f"[click]({url})")
        f = discord.File('assets/npm_logo.png', 'npm.png')
        embed.set_thumbnail(url="attachment://npm.png")
        await ctx.reply(embed=embed, file=f)

    @commands.command(name='deno', description="Shows details of a deno package.", usage="deno <package>")
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def _deno(self, ctx, package: str) -> None:
        async with ctx.typing():
            data = await (await self.bot.session.get(f"https://api.deno.land/modules/{package}")).json()
            if data["success"]:
                data = data['data']
                version = await (await self.bot.session.get(f"https://cdn.deno.land/{data['name']}/meta/versions.json")).json()
                embed = discord.Embed(title=data['name'], description=data['description'],
                                      url=f"https://deno.land/x/{data['name']}", color=0x2F3136)
                embed.add_field(name="Version", value=version['latest'])
                embed.add_field(name="Stars", value=f"{data['star_count']:,}")
                f = discord.File('assets/deno_logo.png', 'deno.png')
                embed.set_thumbnail(url="attachment://deno.png")
                await ctx.reply(embed=embed, file=f)
            else:
                raise commands.BadArgument("Invalid package.")

    @commands.command(name='github', description="Shows details of a deno repository.", usage="github <repository>",
                      aliases=['gh'])
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def _github(self, ctx, repository: str) -> None:
        async with ctx.typing():
            data = await (await self.bot.session.get(f"https://api.github.com/repos/{repository}")).json()
        if 'message' not in data:
            embed = discord.Embed(title=data['full_name'],
                                  url=data['html_url'], color=0x2F3136)
            embed.set_image(
                url=f"https://opengraph.githubassets.com/c76ba569f3d5fd1be198fd9ac5577b03dc2bd09eed29021adfd94e615aad4315/{data['full_name']}")
            await ctx.reply(embed=embed)
        else:
            raise commands.BadArgument("Invalid repository.")

    @commands.command(name='txt', description="Text to file.", usage="txt <text>")
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def _txt(self, ctx, *, text: str) -> None:
        file = io.StringIO()
        file.write(text)
        file.seek(0)
        await ctx.reply(file=discord.File(file, 'output.txt'))

    @commands.command(name='serverinfo', description="Displays info about the server.", aliases=['guildinfo'])
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def _serverinfo(self, ctx):
        description = "" if ctx.guild.description is None else ctx.guild.description
        bots = online = dnd = idle = offline = 0
        for member in ctx.guild.members:
            if member.bot:
                bots += 1
            elif member.raw_status == "online":
                online += 1
            elif member.raw_status == "dnd":
                dnd += 1
            elif member.raw_status == "offline":
                offline += 1
            elif member.raw_status == "idle":
                idle += 1

        try:
            booster_role = ctx.guild.premium_subscriber_role.mention
        except AttributeError:
            booster_role = "N/A"
        created_at = ctx.guild.created_at.strftime("%d/%m/%Y at %H:%M:%S")

        embed = discord.Embed(
            title=ctx.guild.name, description=f"{description}", color=0x2F3136)
        embed.set_image(url=ctx.guild.banner.url if hasattr(
            ctx.guild.banner, 'url') else None)
        embed.set_thumbnail(url=ctx.guild.icon.url if hasattr(
            ctx.guild.icon, 'url') else None)
        embed.add_field(name="Members", value=f"""
Online: `{online}`
DND: `{dnd}`
Idle: `{idle}`
Offline: `{offline}`
Bots: `{bots}`""", inline=True)
        embed.add_field(name="Boosts", value=f"""
Amount: `{ctx.guild.premium_subscription_count}`
Role: {booster_role}""", inline=True)
        embed.add_field(name="Channels", value=f"""
All `{len(ctx.guild.channels)}`
Text: `{len(ctx.guild.text_channels)}`
Voice: `{len(ctx.guild.voice_channels)}`""", inline=True)
        embed.add_field(name="Other", value=f"""
Owner: {ctx.guild.owner.mention}
Roles: `{len(ctx.guild.roles)}`
Region: `{ctx.guild.region}`
Created at: `{created_at}` ({humanize.naturaltime(ctx.guild.created_at)})""", inline=True)

        await ctx.reply(embed=embed)

    @commands.command(name='userinfo', description="Displays info about the user.", usage="userinfo [member]")
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def _userinfo(self, ctx, member: commands.MemberConverter = None):
        member = member or ctx.author

        if str(member.mobile_status) != "offline":
            platform = "Mobile"
        elif str(member.desktop_status) != "offline":
            platform = "Desktop"
        elif str(member.web_status) != "offline":
            platform = "Web"
        else:
            platform = "N/A"

        created_at = member.created_at.strftime("%d/%m/%Y at %H:%M:%S")
        joined_at = member.joined_at.strftime("%d/%m/%Y at %H:%M:%S")

        if member.top_role.name == "@everyone":
            top_role = "N/A"
        else:
            top_role = member.top_role.mention

        join_position = sum(
            member.joined_at > m.joined_at if m.joined_at is not None else "1" for m in ctx.guild.members)

        embed = discord.Embed(title=str(member), color=0x2F3136)
        embed.add_field(name="Info", value=f"""
Name: `{member.name}`
Nickname: `{''.join("N/A" if member.nick is None else member.nick)}`
Status: `{''.join(member.raw_status.title() if member.raw_status != "dnd" else "DND")}`
Platform: `{platform}`
Created at: `{created_at} ({humanize.naturaltime(member.created_at)})`""", inline=True)

        embed.add_field(name="Guild", value=f"""
Roles: `{len(member.roles)}`
Top Role: {top_role}
Join Position: `{join_position}`
Joined at: `{joined_at} ({humanize.naturaltime(member.joined_at)})`""", inline=True)
        embed.set_footer(text=f"ID: {member.id}",
                         icon_url=ctx.author.avatar.url)
        embed.set_thumbnail(url=member.avatar.url)

        await ctx.reply(embed=embed)

    @commands.command(name='tts', description="Text to speech.", usage="tts <text>", aliases=['texttospeech'])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def _tts(self, ctx, *, text: str):
        if len(text) > 200:
            raise commands.BadArgument(
                "The text for text to speech can not be over 200 characters.")

        buffer = io.BytesIO()
        async with ctx.typing():
            await self.tts.write_to_fp(text, buffer, slow=True, lang="en")
        buffer.seek(0)
        await ctx.reply(file=discord.File(buffer, f"{text}.mp3"))

    @commands.command(name='execute', description="Run code.", usage="execute <language> <code>")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def _execute(self, ctx, language: str, *, code: str):
        if code.startswith('```') and code.endswith('```'):
            if code.startswith('```\n') and code.endswith('\n```') in code:
                code = code.split('\n')
                code = code[1:]
                code = code[:-1]
                code = '\n'.join(code)
            elif code.startswith('```\n') and code.endswith('```'):
                code = code.split('\n')
                code = code[1:]
                code = '\n'.join(code)
                code = code[:-3]
            elif code.startswith('```') and code.endswith('\n```'):
                code = code.split('\n')
                code = code[:-1]
                code = '\n'.join(code)
                code = code[3:]
            else:
                code = code[3:]
                code = code[:-3]
        elif code.startswith('`') and code.endswith('`'):
            code = code[1:]
            code = code[:-1]
        output = await self.tio.execute(code, language=language)
        await ctx.reply(embed=discord.Embed(description=f"```\n{output}\n```", color=0x2F3136))


def setup(bot) -> None:
    bot.add_cog(Utility(bot))
