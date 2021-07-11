import discord
from discord.ext import commands
from utils.music import YTDLError, Song, YTDLSource
from jishaku.codeblocks import codeblock_converter
import io
import humanize


class Utility(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.command(name='avatar', description="Shows a user's avatar.", usage="avatar [member]")
    async def _avatar(self, ctx: commands.Context, member: commands.MemberConverter = None) -> None:
        member = member or ctx.author
        embed = discord.Embed(
            description=f"[png]({member.avatar_url_as(static_format='png')}) | [jpg]({member.avatar_url_as(static_format='jpg')}) | [webp]({member.avatar_url_as(static_format='webp')})",
            color=0x2F3136)
        embed.set_image(url=member.avatar_url_as(static_format='png'))
        await ctx.reply(embed=embed)

    @commands.command(name='pypi', description="Shows details of a python package.", usage="pypi <package>")
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def _pypi(self, ctx: commands.Context, package: str) -> None:
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
    async def _npm(self, ctx: commands.Context, package: str):
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
    async def _deno(self, ctx: commands.Context, package: str) -> None:
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
    async def _github(self, ctx: commands.Context, repository: str) -> None:
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
    async def _txt(self, ctx: commands.Context, *, text: str) -> None:
        file = io.StringIO()
        file.write(text)
        file.seek(0)
        await ctx.reply(file=discord.File(file, 'output.txt'))

    @commands.command(name='tts', description="Text to speech.", usage="tts <text>", aliases=['texttospeech'])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def _tts(self, ctx: commands.Context, *, text: str) -> None:
        if len(text) > 200:
            raise commands.BadArgument(
                "The text for text to speech can not be over 200 characters.")

        buffer = io.BytesIO()
        async with ctx.typing():
            await self.tts.write_to_fp(text, buffer, slow=True, lang="en")
        buffer.seek(0)
        await ctx.reply(file=discord.File(buffer, f"{text}.mp3"))

    @commands.command(name='youtube')
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def _youtube(self, ctx: commands.Context, query: str) -> None:
        async with ctx.typing():
            try:
                source = await YTDLSource.create_source(ctx, query, loop=self.bot.loop)
            except YTDLError as e:
                await ctx.reply('An error occurred while processing this request: {}'.format(str(e)))
            else:
                song = Song(source)

                await ctx.voice_state.songs.put(song)
                await ctx.reply('Enqueued {}'.format(str(source)))

    @commands.command(name='execute', description="Run code.", usage="execute <language> <code>")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def _execute(self, ctx: commands.Context, language: str, *, code: codeblock_converter) -> None:
        async with ctx.typing():
            output = await self.bot.tio.execute(code.content, language=language)
        await ctx.reply(embed=discord.Embed(description=f"```\n{str(output)[:200]}\n```", color=0x2F3136))


def setup(bot) -> None:
    bot.add_cog(Utility(bot))
