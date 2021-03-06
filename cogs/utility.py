import io
import json
import random
from typing import Optional

import discord
from async_tio import LanguageNotFound
from discord.ext import commands

from jishaku.codeblocks import codeblock_converter
from utils.context import ApolloContext
from utils.metrics import Embed


class Utility(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot
        self._cd_type = commands.BucketType.user
        self._cd = commands.CooldownMapping.from_cooldown(
            1, 2.5, self._cd_type)

    async def cog_check(self, ctx: ApolloContext):
        bucket = self._cd.get_bucket(ctx.message)
        retry_after = bucket.update_rate_limit()
        if retry_after:
            raise commands.CommandOnCooldown(
                self._cd, retry_after, self._cd_type)
        else:
            return True

    @commands.command(name='pypi', description="Shows details of a python package.", usage="<package>")
    async def _pypi(self, ctx: ApolloContext, package: commands.clean_content) -> None:
        data = await self.bot.session.get(f"https://pypi.org/pypi/{package}/json")

        if data.status != 200:
            raise commands.UserInputError("Invalid package.")

        data = (await data.json())['info']
        embed = Embed(
            title=data['name'], description=data.get('summary', ''), url=data.get('project_url', 'https://pypi.org/'))
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

    @commands.command(name='npm', description="Shows details of a node package.", usage="<package>")
    async def _npm(self, ctx: ApolloContext, package: commands.clean_content):
        data = await (await self.bot.session.get(f"https://api.npms.io/v2/package/{package}")).json()
        if 'CODE' in data or 'collected' not in data:
            raise commands.UserInputError("Invalid package.")

        data = data['collected']['metadata']
        embed = Embed(title=data['name'], description=data.get(
            'description', ''), url=data['links']['npm'])
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

    @commands.command(name='deno', description="Shows details of a deno package.", usage="<package>")
    async def _deno(self, ctx: ApolloContext, package: commands.clean_content) -> None:
        data = await (await self.bot.session.get(f"https://api.deno.land/modules/{package}")).json()
        if data["success"]:
            data = data['data']
            version = await (
                await self.bot.session.get(f"https://cdn.deno.land/{data['name']}/meta/versions.json")).json()
            embed = Embed(title=data['name'], description=data['description'],
                          url=f"https://deno.land/x/{data['name']}")
            embed.add_field(name="Version", value=version['latest'])
            embed.add_field(name="Stars", value=f"{data['star_count']:,}")
            f = discord.File('assets/deno_logo.png', 'deno.png')
            embed.set_thumbnail(url="attachment://deno.png")
            await ctx.reply(embed=embed, file=f)
        else:
            raise commands.UserInputError("Invalid package.")

    @commands.command(name='txt', description="Text to file.", usage="<text>")
    async def _txt(self, ctx: ApolloContext, *, text: str) -> None:
        file = io.StringIO()
        file.write(text)
        file.seek(0)
        await ctx.reply(file=discord.File(file, 'output.txt'))

    @commands.command(name='tts', description="Text to speech.", usage="<text>", aliases=['texttospeech'])
    async def _tts(self, ctx: ApolloContext, *, text: commands.clean_content) -> None:
        if len(text) > 1000:
            raise commands.UserInputError(
                "The text for text to speech can not be over 200 characters.")

        buffer = io.BytesIO()
        await self.bot.tts.write_to_fp(text, buffer, slow=True, lang="en")
        buffer.seek(0)
        await ctx.reply(file=discord.File(buffer, f"{text}.mp3"))

    @commands.command(name='execute', description="Run code.", usage="<language> <code>")
    async def _execute(self, ctx: ApolloContext, language: commands.clean_content, *,
                       code: codeblock_converter) -> None:
        try:
            output = await self.bot.tio.execute(code.content, language=language)
            await ctx.reply(embed=Embed(description=f"```\n{str(output)[:500]}\n```"))
        except LanguageNotFound as e:
            raise commands.UserInputError(e)

    @commands.command(name='avatar', description="View the avatar of a member.", usage="[member]")
    async def _avatar(self, ctx: ApolloContext, member: Optional[commands.UserConverter] = None):
        member = member or ctx.author
        formats = [f"[`PNG`]({member.avatar.replace(format='png').url})"]
        formats.append(
            f"[`JPG`]({member.avatar.replace(format='jpg').url})")
        formats.append(
            f"[`JPEG`]({member.avatar.replace(format='jpeg').url})")
        formats.append(
            f"[`WEBP`]({member.avatar.replace(format='webp').url})")
        if member.avatar.is_animated():
            formats.append(
                f"[`GIF`]({member.avatar.replace(format='gif').url})")
        embed = Embed(title=f"{member.name}'s avatar", description=' | '.join(
            formats))
        embed.set_image(url=member.avatar.url)
        await ctx.reply(embed=embed)

    @commands.command(name='rawmsg', description="Get the raw json of a message.", usage="[message]")
    async def _rawmsg(self, ctx: ApolloContext, message: Optional[commands.MessageConverter] = None) -> None:
        message = message or ctx.message.reference

        if not message:
            raise commands.UserInputError(
                "You didn't reply or specify a message.")

        
        if hasattr(message, 'resolved'):
            message = message.resolved

        raw_message = await self.bot.http.get_message(message.channel.id, message.id)
        raw_message = json.dumps(raw_message, indent=4)
        await ctx.reply(f"```json\n{raw_message}\n```")

    @commands.command(name='random', description="Shows a random number between 0 and 1.")
    async def _random(self, ctx: ApolloContext):
        await ctx.reply(str(random.random()))

# TODO userinfo command
# TODO serverinfo command


def setup(bot) -> None:
    bot.add_cog(Utility(bot))
